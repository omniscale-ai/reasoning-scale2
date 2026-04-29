#!/usr/bin/env python3
"""Run the planning self-correction experiment."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.runner import Runner


def main():
    parser = argparse.ArgumentParser(description="Run reasoning-scale experiment")
    parser.add_argument("--config", default="config/experiment_v1.yaml", help="Path to config YAML")
    args = parser.parse_args()

    runner = Runner(args.config)
    runner.run()


if __name__ == "__main__":
    main()
