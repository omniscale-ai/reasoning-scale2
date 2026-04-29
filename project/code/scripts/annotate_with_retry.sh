#!/bin/bash
# Runs collect_and_annotate.py and automatically restarts on crash.
# Safe to restart because the script checkpoints completed tasks to JSONL.

TASKS_PER_SOURCE=${1:-25}
LOG=${2:-/tmp/annotate.log}
MAX_ATTEMPTS=50   # hard ceiling to prevent infinite loops
DELAY=5           # seconds between restarts

echo "$(date): Starting annotation (tasks-per-source=$TASKS_PER_SOURCE)"
echo "$(date): Log: $LOG"
echo "$(date): Checkpointed results: data/annotation_pilot/tasks_annotated.jsonl"

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
    attempt=$((attempt + 1))
    echo "$(date): Attempt $attempt / $MAX_ATTEMPTS" | tee -a "$LOG"

    python scripts/collect_and_annotate.py --tasks-per-source "$TASKS_PER_SOURCE" 2>&1 | tee -a "$LOG"
    EXIT=$?

    if [ $EXIT -eq 0 ]; then
        echo "$(date): Completed successfully after $attempt attempt(s)." | tee -a "$LOG"
        exit 0
    fi

    echo "$(date): Exited with code $EXIT, restarting in ${DELAY}s..." | tee -a "$LOG"
    sleep $DELAY
done

echo "$(date): Reached max attempts ($MAX_ATTEMPTS). Giving up." | tee -a "$LOG"
exit 1
