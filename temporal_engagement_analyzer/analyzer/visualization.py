import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class HeatmapVisualizer:
    @staticmethod
    def plot(summary: dict, title: str = "Engagement Heatmaps"):
        rows = []
        for (day, hour), metrics in summary.items():
            rows.append({
                "day": day,
                "hour": hour,
                "avg_replies": metrics["avg_replies"],
                "avg_reactions": metrics["avg_reactions"]
            })

        df = pd.DataFrame(rows)

        # Full grid
        day_order = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"
        ]
        full_hours = list(range(24))

        # Pivot tables
        pivot_replies = df.pivot(
            index="day",
            columns="hour",
            values="avg_replies"
        ).reindex(index=day_order, columns=full_hours).fillna(-2)

        pivot_reactions = df.pivot(
            index="day",
            columns="hour",
            values="avg_reactions"
        ).reindex(index=day_order, columns=full_hours).fillna(-2)

        # Create plots
        fig, axes = plt.subplots(1, 2, figsize=(18, 6))

        sns.heatmap(
            pivot_replies,
            ax=axes[0],
            cmap="viridis",
            linewidths=0.5
        )
        axes[0].set_title("Avg Replies")
        axes[0].set_xlabel("Hour of Day")
        axes[0].set_ylabel("Day of Week")

        sns.heatmap(
            pivot_reactions,
            ax=axes[1],
            cmap="viridis",
            linewidths=0.5
        )
        axes[1].set_title("Avg Reactions")
        axes[1].set_xlabel("Hour of Day")
        axes[1].set_ylabel("")

        fig.suptitle(title)
        plt.tight_layout()
        plt.show()