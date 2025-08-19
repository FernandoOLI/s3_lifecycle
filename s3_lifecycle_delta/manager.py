# s3_lifecycle_delta/manager.py

import json
from typing import Optional
import boto3

from .policy import LifecyclePolicy
from .diff import DiffResult, RuleChange
from .validators import validate_policy
from .exceptions import ApplyError, DiffError


class LifecycleManager:
    def __init__(self, s3_client: Optional[boto3.client] = None):
        self.s3 = s3_client or boto3.client("s3")

    def fetch_current(self, bucket_name: str) -> LifecyclePolicy:
        try:
            resp = self.s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
            return LifecyclePolicy.from_dict({"Rules": resp.get("Rules", [])})
        except self.s3.exceptions.NoSuchLifecycleConfiguration:
            return LifecyclePolicy(Rules=[])
        except Exception as e:
            raise ApplyError(f"failed to fetch current lifecycle: {e}") from e

    @staticmethod
    def _normalize_dict(d: dict) -> dict:
        return json.loads(json.dumps(d, sort_keys=True))

    def compute_delta(self, bucket_name: str, desired_policy: LifecyclePolicy) -> DiffResult:
        try:
            current = self.fetch_current(bucket_name)
        except Exception as e:
            raise DiffError(f"Failed to fetch current lifecycle for diff: {e}") from e

        to_add = []
        to_delete = []
        to_update = []

        current_rules = {r.ID: r for r in current.Rules}
        desired_rules = {r.ID: r for r in desired_policy.Rules}

        for rid, desired_rule in desired_rules.items():
            if rid not in current_rules:
                to_add.append(desired_rule)
            else:
                cur_norm = self._normalize_dict(current_rules[rid].model_dump())
                des_norm = self._normalize_dict(desired_rule.model_dump())
                if cur_norm != des_norm:
                    to_update.append({"before": current_rules[rid], "after": desired_rule})

        for rid, current_rule in current_rules.items():
            if rid not in desired_rules:
                to_delete.append(current_rule)

        rule_change = RuleChange(to_add=to_add, to_update=to_update, to_delete=to_delete)
        return DiffResult(rule_change)

    def apply_delta(
        self,
        bucket_name: str,
        delta: DiffResult,
        desired_policy: LifecyclePolicy,
        dry_run: bool = True
    ) -> None:
        validate_policy(desired_policy)
        summary = delta.summary()
        print(f"[apply_delta] Delta summary: {summary}")
        if dry_run:
            print("[apply_delta] Dry-run mode; not applying changes.")
            return

        try:
            self.s3.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration=desired_policy.dict()
            )
        except Exception as e:
            raise ApplyError(f"Failed to apply lifecycle policy: {e}") from e
