import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Dict, Tuple

SummaryKey = Tuple[str, int]


class HeatmapVisualizer:
    # Configuration for plots: (title, column, colormap)
    PLOTS = [
        ("Avg Replies", "avg_replies", "viridis"),
        ("Avg Reactions", "avg_reactions", "viridis"),
        ("Median Replies", "median_replies", "magma"),
        ("Median Reactions", "median_reactions", "magma"),
    ]

    DAY_ORDER = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    HOURS = list(range(24))
    MISSING_VALUE = -2  # keep your original behavior explicit

    @staticmethod
    def _to_dataframe(summary: Dict[SummaryKey, dict]) -> pd.DataFrame:
        rows = [
            {
                "day": day,
                "hour": hour,
                **metrics
            }
            for (day, hour), metrics in summary.items()
        ]
        return pd.DataFrame(rows)

    @classmethod
    def _pivot(cls, df: pd.DataFrame, value: str) -> pd.DataFrame:
        return (
            df.pivot(index="day", columns="hour", values=value)
            .reindex(index=cls.DAY_ORDER, columns=cls.HOURS)
            .fillna(cls.MISSING_VALUE)
        )

    @classmethod
    def plot(
        cls,
        summary: Dict[SummaryKey, dict],
        title: str = "Engagement Heatmaps"
    ) -> Figure:
        df = cls._to_dataframe(summary)

        n_plots = len(cls.PLOTS)
        n_cols = 2
        n_rows = (n_plots + 1) // n_cols

        fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 3 * n_rows))
        axes = axes.flatten()  # normalize for easy iteration

        for ax, (plot_title, column, cmap) in zip(axes, cls.PLOTS):
            pivot = cls._pivot(df, column)

            sns.heatmap(
                pivot,
                ax=ax,
                cmap=cmap,
                linewidths=0.5
            )

            ax.set_title(plot_title)
            ax.set_xlabel("Hour of Day")
            ax.set_ylabel("Day of Week")

        # Hide unused axes (if any)
        for ax in axes[n_plots:]:
            ax.set_visible(False)

        fig.suptitle(title)
        plt.tight_layout()

        return fig