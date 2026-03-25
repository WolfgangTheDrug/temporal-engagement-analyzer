import argparse

from analyzer.file_scanner import FileScanner
from analyzer.slack_parser import SlackParser
from analyzer.aggregator import MetricsAggregator


def main():
    parser = argparse.ArgumentParser(description="Slack Export Analyzer")
    parser.add_argument("path", help="Path to root folder")

    args = parser.parse_args()

    scanner = FileScanner(args.path)
    files = scanner.get_json_files()

    aggregator = MetricsAggregator()

    for file_path in files:
        try:
            messages = SlackParser.parse_file(file_path)
            aggregator.add_messages(messages)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    summary = aggregator.summary()

    print("\n=== Summary ===")
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()