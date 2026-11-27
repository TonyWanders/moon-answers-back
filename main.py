#!/usr/bin/env python3
"""One line in the voice of the Moon answering back.

Writes the fixed line to /output/entry.txt, or to the path given as the
first argument, or to $OUTPUT_PATH. Deterministic: no network, no clock,
no randomness. The competition gate is 1 to 240 characters and the line
must not be only white space.
"""

import os
import sys
from pathlib import Path

TEXT = "I heard every wish. I granted none of them. I am a rock with good lighting and no customer service."

MIN_LENGTH = 1
MAX_LENGTH = 240
FALLBACK_PATH = "/output/entry.txt"


class LineEntry:
    """One competition line, with the gate it has to pass and the write."""

    def __init__(self, text: str) -> None:
        self.text = text

    def char_count(self) -> int:
        return len(self.text)

    def validate(self) -> None:
        """Enforce the 1-240 character gate. Raises ValueError if it fails."""
        count = self.char_count()
        if count < MIN_LENGTH or count > MAX_LENGTH:
            raise ValueError(f"line is {count} characters, outside 1-240")
        if not self.text.strip():
            raise ValueError("line is only white space")

    def store(self, path: Path) -> int:
        """Write the line exactly as it is, no trailing newline added.

        Returns the number of bytes written.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.text, encoding="utf-8")
        path.chmod(0o644)  # make.fun collects outputs as another user
        return len(self.text.encode("utf-8"))


def resolve_output_path(argv: list[str]) -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(argv) > 1:
        return Path(argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(FALLBACK_PATH)


def run(argv: list[str]) -> int:
    entry = LineEntry(TEXT)
    try:
        entry.validate()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    target = resolve_output_path(argv)
    written = entry.store(target)
    print(f"wrote {written} bytes ({entry.char_count()} characters) to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv))
