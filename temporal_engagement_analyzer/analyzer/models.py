from dataclasses import dataclass
from datetime import datetime

@dataclass
class MessageMetrics:
    ts: str
    datetime: datetime
    reply_count: int
    reply_user_count: int
    reactions_count: int