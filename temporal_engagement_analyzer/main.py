import argparse

from .analyzer.file_scanner import FileScanner
from .analyzer.slack_parser import SlackParser
from .analyzer.aggregator import MetricsAggregator
from .analyzer.time_aggregator import TimeAggregator

def main():
    parser = argparse.ArgumentParser(description="Slack Export Analyzer")
    parser.add_argument("path", help="Path to root folder")

    args = parser.parse_args()

    scanner = FileScanner(args.path)
    files = scanner.get_json_files()

    aggregator = MetricsAggregator()
    time_aggregator = TimeAggregator()

    for file_path in files:
        try:
            messages = SlackParser.parse_file(file_path)
            aggregator.add_messages(messages)
            time_aggregator.add(messages)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    summary = aggregator.summary()

    print("\n=== Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")

    results = time_aggregator.summary()
    for (day, hour), metrics in sorted(results.items()):
        print(f"{day} {hour:02d}:00")
        print(f"  Messages: {metrics['message_count']}")
        print(f"  Avg replies: {metrics['avg_replies']:.2f}")
        print(f"  Avg reactions: {metrics['avg_reactions']:.2f}")
        print()


if __name__ == "__main__":
    main()