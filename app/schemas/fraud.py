from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class FraudCheckRequest:
    message: str


@dataclass
class FraudCheckResponse:
    suspicious: bool
    risk_score: int
    matches: List[str] = field(default_factory=list)
    cleaned_message: str = ""
