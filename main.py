#!/usr/bin/env python3
"""Write the one-line pitch to /output/entry.txt."""

from pathlib import Path

ENTRY = (
    "Your idea can stay yours: tell an AI agent on make.fun what your first app should do, "
    "in the words you'd use over coffee, and try the first version it builds before you "
    "decide it deserves a weekend."
)

OUTPUT = Path("/output/entry.txt")
MAX_CHARS = 240


def validate(data):
    """Return valid UTF-8 entry text, or raise ValueError."""
    if isinstance(data, bytes):
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("entry must be UTF-8 text") from exc
    elif isinstance(data, str):
        text = data
    else:
        raise TypeError("entry must be text or UTF-8 bytes")

    count = len(text)
    if not 1 <= count <= MAX_CHARS:
        raise ValueError(f"entry must be 1 to {MAX_CHARS} characters, got {count}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if any(ord(char) < 32 or (char.isspace() and char != " ") for char in text):
        raise ValueError("entry must be one printed line")
    if "make.fun" not in text:
        raise ValueError("entry must name make.fun")
    return text


def write_entry(output=None):
    """Validate ENTRY and write its exact UTF-8 bytes to the output file."""
    text = validate(ENTRY.encode("utf-8"))
    target = OUTPUT if output is None else Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = text.encode("utf-8")
    target.write_bytes(payload)
    return payload


def main():
    payload = write_entry()
    print(f"wrote {len(payload)} bytes to {OUTPUT}")


if __name__ == "__main__":
    main()
