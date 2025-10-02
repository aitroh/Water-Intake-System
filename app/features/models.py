from dataclasses import dataclass
from datetime import datetime

@dataclass
class WaterLog:
    id: int
    amount: int   # in ml
    timestamp: datetime