"""The Excuse That Almost Works — make.fun entry.

Writes one line (at most 20 words, 1-140 characters): the excuse a gamer
texts the boss to skip work on GTA 6 launch week, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Pure standard library only.

Why this line: it is a boring, believable excuse — the car won't start —
until its own last words collapse it. The gamer killed his own car battery
charging a game controller for the midnight launch, so the excuse confesses
even as it is made. A tired manager almost believes it for a second, then
the "midnight launch" gives the game away.
"""

import os

LINE = (
    "Sorry, car won't start, I left it charging my controller "
    "all night for the midnight launch."
)

MAX_CHARS = 140
MAX_WORDS = 20


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-140 chars, not only whitespace,
    a single line, at most 20 words, and no control characters."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 140-char limit" % len(text))
    if len(text.split()) > MAX_WORDS:
        raise ValueError(
            "entry is %d words, over the 20-word limit" % len(text.split())
        )
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(LINE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d, words: %d" % (len(entry), len(entry.split())))


if __name__ == "__main__":
    main()
