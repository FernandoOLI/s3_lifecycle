import pytest
from s3_lifecycle_delta.policy import LifecyclePolicy
from s3_lifecycle_delta.validators import validate_policy
from pydantic import ValidationError as PydanticValidationError

def test_valid_transition_days_pass():
    policy = LifecyclePolicy.from_dict({
        "Rules": [
            {
                "ID": "valid-rule",
                "Filter": {"Prefix": "data/"},
                "Status": "Enabled",
                "Transitions": [
                    {"Days": 30, "StorageClass": "STANDARD_IA"},
                    {"Days": 90, "StorageClass": "GLACIER"}
                ]
            }
        ]
    })
    validate_policy(policy)  # Should not raise

def test_invalid_transition_days_fail():
    with pytest.raises(PydanticValidationError):
        LifecyclePolicy.from_dict({
            "Rules": [
                {
                    "ID": "invalid-rule",
                    "Filter": {"Prefix": "data/"},
                    "Sttatus": "Enabled",
                    "Transitions": [
                        {"Days": 90, "StorageClass": "GLACIER"},
                        {"Days": 30, "StorageClass": "STANDARD_IA"}
                    ]
                }
            ]
        })

def test_empty_rule_rejected():
    with pytest.raises(Exception):  # Pydantic ValidationError
        LifecyclePolicy.from_dict({
            "Rules": [
                {
                    "ID": "bad-rule",
                    "Filter": {"Prefix": "data/"},
                    "Status": "Enabled"
                }
            ]
        })