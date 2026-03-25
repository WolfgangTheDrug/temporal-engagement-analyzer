from dataclasses import dataclass

@dataclass
class MessageMetrics:
    ts: str
    reply_count: int
    reply_user_count: int
    reactions_count: int