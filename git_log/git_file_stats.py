#!/usr/bin/env python3
"""
git_file_stats.py - Analyze git log file and count file commit frequencies

This script parses a git log file and counts how many times each file appears in commits.
Results are displayed in ascending order by commit count.
"""
import re
from collections import defaultdict
from pathlib import Path


class GitLogAnalyzer:
    """Analyze git log files to extract file commit statistics."""

    def __init__(self, log_file_path):
        """Initialize with the path to the git log file."""
        self.log_file_path = Path(log_file_path)
        self.file_counts = defaultdict(int)

    def parse_log_file(self):
        """Parse the git log file and count file occurrences."""
        # Use a generator to process the file line by line without loading it all into memory
        for line in self._read_log_file():
            # Skip commit headers, author lines, dates, and empty lines
            if (line.startswith('commit ') or
                line.startswith('Author: ') or
                line.startswith('Date: ') or
                not line.strip()):
                continue

            # Skip commit message lines (they're indented with 4 spaces)
            if line.startswith('    '):
                continue

            # File lines have the format: "N   M   filepath" where N and M are numbers
            # representing additions and deletions
            parts = line.strip().split('\t')
            if len(parts) == 3 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                # Extract the filename
                filename = parts[2].strip()
                # Handle rename syntax: {old_name => new_name}
                if '=>' in filename:
                    # For renames, count the new name
                    filename = filename.split('=>')[1].strip()

                self.file_counts[filename] += 1

    def _read_log_file(self):
        """Generator to read the log file line by line."""
        with open(self.log_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                yield line

    def get_sorted_results(self):
        """Return the results sorted by commit count (ascending)."""
        return sorted(self.file_counts.items(), key=lambda x: x[1])

    def display_results(self):
        """Display the results in a formatted way."""
        sorted_results = self.get_sorted_results()

        if not sorted_results:
            print("No files found in the git log.")
            return

        # Find the maximum filename length for formatting
        max_filename_length = max(len(filename) for filename, _ in sorted_results)
        max_count_length = max(len(str(count)) for _, count in sorted_results)

        # Print header
        print(f"{'Count':<{max_count_length}} | {'Filename':<{max_filename_length}}")
        print(f"{'-' * max_count_length}-+-{'-' * max_filename_length}")

        # Print each file with its commit count
        for filename, count in sorted_results:
            print(f"{count:<{max_count_length}} | {filename}")

        # Print summary
        total_files = len(sorted_results)
        total_commits = sum(count for _, count in sorted_results)
        print(f"\nTotal unique files: {total_files}")
        print(f"Total file commits: {total_commits}")


def main():
    """Main function to run the analysis."""
    log_file_path = "git_log.txt"

    analyzer = GitLogAnalyzer(log_file_path)
    analyzer.parse_log_file()
    analyzer.display_results()


if __name__ == "__main__":
    main()