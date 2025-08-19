from typing import List, Optional, Dict, Any
from pydantic import BaseModel, model_validator


class Transition(BaseModel):
    Date: Optional[str] = None
    Days: Optional[int] = None
    StorageClass: str

    @model_validator(mode="after")
    def check_date_or_days(cls, values):
        if not values.Date and values.Days is None:
            raise ValueError("Either Date or Days must be provided")
        return values


class Expiration(BaseModel):
    Days: Optional[int]
    Date: Optional[str]


class Filter(BaseModel):
    Prefix: Optional[str] = None
    # Extend later for Tag-based filters


class Rule(BaseModel):
    ID: str
    Filter: dict
    Status: str
    Transitions: Optional[List[Transition]] = None
    Expiration: Optional[dict] = None

    @model_validator(mode="after")
    def check_rule_not_empty(self):
        # Must have at least one of Transitions or Expiration
        if not self.Transitions and not self.Expiration:
            raise ValueError(f"Rule '{self.ID}' must have at least Transitions or Expiration")
        return self


class LifecyclePolicy(BaseModel):
    Rules: List[Rule]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LifecyclePolicy":
        return cls.model_validate(d)
