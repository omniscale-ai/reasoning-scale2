#!/bin/bash
# Runs run_diploma_experiments.py with auto-restart on crash.
ARGS="${@:---exp 1 2 3 5}"
LOG=/tmp/diploma_exp.log
MAX_ATTEMPTS=30
DELAY=5

echo "$(date): Starting diploma experiments (args: $ARGS)" | tee -a "$LOG"

attempt=0
while [ $attempt -lt $MAX_ATTEMPTS ]; do
    attempt=$((attempt + 1))
    echo "$(date): Attempt $attempt / $MAX_ATTEMPTS" | tee -a "$LOG"

    python scripts/run_diploma_experiments.py $ARGS 2>&1 | tee -a "$LOG"
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
