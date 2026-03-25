from typing import List

from .models import MessageMetrics

class MetricsAggregator:
    def __init__(self):
        self.messages: List[MessageMetrics] = []

    def add_messages(self, messages: List[MessageMetrics]):
        self.messages.extend(messages)

    def summary(self) -> dict:
        total_messages = len(self.messages)
        total_replies = sum(m.reply_count for m in self.messages)
        total_reply_users = sum(m.reply_user_count for m in self.messages)
        total_reactions = sum(m.reactions_count for m in self.messages)

        return {
            "total_messages": total_messages,
            "total_replies": total_replies,
            "total_reply_users": total_reply_users,
            "total_reactions": total_reactions,
        }