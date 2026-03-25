from collections import defaultdict
from typing import List, Dict

from .models import MessageMetrics


class TimeAggregator:
    def __init__(self):
        self.data = defaultdict(lambda: {
            "messages": 0,
            "replies": 0,
            "reactions": 0
        })

    def add(self, messages: List[MessageMetrics]):
        for msg in messages:
            key = self._get_key(msg)

            self.data[key]["messages"] += 1
            self.data[key]["replies"] += msg.reply_count
            self.data[key]["reactions"] += msg.reactions_count

    def _get_key(self, msg: MessageMetrics):
        return (
            msg.datetime.strftime("%A"),  # Monday, Tuesday...
            msg.datetime.hour             # 0–23
        )

    def summary(self) -> Dict:
        result = {}

        for key, values in self.data.items():
            day, hour = key
            messages = values["messages"]

            result[key] = {
                "avg_replies": values["replies"] / messages,
                "avg_reactions": values["reactions"] / messages,
                "message_count": messages
            }

        return result