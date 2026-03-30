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
                "avg_reactions": metrics["avg_reactions"],
                "median_replies": metrics["median_replies"],
                "median_reactions": metrics["median_reactions"],
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

        pivot_median_replies = df.pivot(
            index="day",
            columns="hour",
            values="median_replies"
        ).reindex(index=day_order, columns=full_hours).fillna(-2)

        pivot_median_reactions = df.pivot(
            index="day",
            columns="hour",
            values="median_reactions"
        ).reindex(index=day_order, columns=full_hours).fillna(-2)

        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=(18, 6))

        # Avg Replies
        sns.heatmap(pivot_replies, ax=axes[0, 0], cmap="viridis", linewidths=0.5)
        axes[0, 0].set_title("Avg Replies")

        # Avg Reactions
        sns.heatmap(pivot_reactions, ax=axes[0, 1], cmap="viridis", linewidths=0.5)
        axes[0, 1].set_title("Avg Reactions")

        # Median Replies
        sns.heatmap(pivot_median_replies, ax=axes[1, 0], cmap="magma", linewidths=0.5)
        axes[1, 0].set_title("Median Replies")

        # Median Reactions
        sns.heatmap(pivot_median_reactions, ax=axes[1, 1], cmap="magma", linewidths=0.5)
        axes[1, 1].set_title("Median Reactions")
        
        for ax in axes.flat:
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Day of Week")

        fig.suptitle(title)
        plt.tight_layout()
        plt.show()