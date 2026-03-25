import json
from typing import List

from .models import MessageMetrics

class SlackParser:
    @staticmethod
    def parse_file(file_path: str) -> List[MessageMetrics]:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        messages = []

        for msg in data:
            if not SlackParser._is_top_level_message(msg):
                continue

            metrics = MessageMetrics(
                ts=msg.get("ts"),
                reply_count=msg.get("reply_count", 0),
                reply_user_count=msg.get("reply_user_count", 0),
                reactions_count=SlackParser._count_reactions(msg),
            )

            messages.append(metrics)

        return messages

    @staticmethod
    def _is_top_level_message(msg: dict) -> bool:
        thread_ts = msg.get("thread_ts")
        ts = msg.get("ts")

        if thread_ts is None:
            return True

        return thread_ts == ts

    @staticmethod
    def _count_reactions(msg: dict) -> int:
        reactions = msg.get("reactions", [])
        return sum(r.get("count", 0) for r in reactions)