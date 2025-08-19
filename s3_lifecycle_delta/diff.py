from typing import List, Dict, Any
from .policy import Rule
from dataclasses import dataclass


@dataclass
class RuleChange:
    to_add: List[Rule]
    to_update: List[Dict[str, Any]]  # could include before/after
    to_delete: List[Rule]

    def summary(self) -> str:
        parts = []
        if self.to_add:
            parts.append(f"Add {len(self.to_add)} rule(s): {[r.ID for r in self.to_add]}")
        if self.to_update:
            parts.append(f"Update {len(self.to_update)} rule(s)")
        if self.to_delete:
            parts.append(f"Delete {len(self.to_delete)} rule(s): {[r.ID for r in self.to_delete]}")
        return "; ".join(parts) if parts else "No changes"


class DiffResult:
    def __init__(self, rule_change: RuleChange):
        self.rule_change = rule_change

    def summary(self) -> str:
        return self.rule_change.summary()
