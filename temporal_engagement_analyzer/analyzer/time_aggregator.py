from collections import defaultdict
from typing import List, Dict
import statistics

from .models import MessageMetrics

class BucketStats:
    def __init__(self):
        self.messages = 0
        self.replies = []
        self.reactions = []

    def add(self, msg):
        self.messages += 1
        self.replies.append(msg.reply_count)
        self.reactions.append(msg.reactions_count)

    def summary(self):
        return {
            "message_count": self.messages,
            "avg_replies": sum(self.replies) / self.messages,
            "avg_reactions": sum(self.reactions) / self.messages,
            "median_replies": statistics.median(self.replies),
            "median_reactions": statistics.median(self.reactions),
        }

class TimeAggregator:
    def __init__(self):
        self.data = defaultdict(BucketStats)

    def add(self, messages: List[MessageMetrics]):
        for msg in messages:
            key = self._get_key(msg)
            self.data[key].add(msg)

    def _get_key(self, msg: MessageMetrics):
        return (
            msg.datetime.strftime("%A"),
            msg.datetime.hour
        )

    def summary(self) -> Dict:
        return {
            key: stats.summary()
            for key, stats in self.data.items()
        }