from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class BaseOrder(ABC):
    id: int
    locations: List[str]
    created_at: float
    status: str
    estimated_compleation_time: float

