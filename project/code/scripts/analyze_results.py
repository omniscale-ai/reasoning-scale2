#!/usr/bin/env python3
"""Analyze experiment results and print metrics table."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.analysis.report import generate_report


def main():
    parser = argparse.ArgumentParser(description="Analyze reasoning-scale results")
    parser.add_argument(
        "--results-dir",
        default="data/results/v1_frontierscience_olympiad",
        help="Path to results directory containing probes.jsonl",
    )
    args = parser.parse_args()

    generate_report(args.results_dir)


if __name__ == "__main__":
    main()
