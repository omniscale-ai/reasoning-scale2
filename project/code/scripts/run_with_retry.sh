#!/bin/bash
# Runs the experiment and automatically restarts on crash until complete.
CONFIG=${1:-config/experiment_full.yaml}
LOG=${2:-/tmp/exp_full.log}

echo "Starting experiment: $CONFIG"
echo "Log: $LOG"

while true; do
    python scripts/run_experiment.py --config "$CONFIG" >> "$LOG" 2>&1
    EXIT=$?
    if [ $EXIT -eq 0 ]; then
        echo "$(date): Experiment completed successfully."
        break
    fi
    echo "$(date): Process exited with code $EXIT, restarting in 3 seconds..."
    sleep 3
done
