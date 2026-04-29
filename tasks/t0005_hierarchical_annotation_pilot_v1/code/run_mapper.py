"""Step 2 driver: run the mapper over the entire pilot file and write
`code/_outputs/mapped.jsonl`.

Usage:
    uv run python -m tasks.t0005_hierarchical_annotation_pilot_v1.code.run_mapper
"""

from __future__ import annotations

import json

from tasks.t0005_hierarchical_annotation_pilot_v1.code.hierarchy_mapper import (
    iter_mapped_rows,
)
from tasks.t0005_hierarchical_annotation_pilot_v1.code.paths import (
    CODE_OUTPUTS_DIR,
    MAPPED_OUTPUT,
    PILOT_INPUT,
)


def main() -> None:
    CODE_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    with MAPPED_OUTPUT.open("w", encoding="utf-8") as out:
        for mapped_row in iter_mapped_rows(input_path=PILOT_INPUT):
            out.write(json.dumps(mapped_row, ensure_ascii=False))
            out.write("\n")
            written += 1
    print(f"Wrote {written} mapped rows to {MAPPED_OUTPUT}")


if __name__ == "__main__":
    main()
