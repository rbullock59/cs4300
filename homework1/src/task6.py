"""Task 6: file handling."""

from pathlib import Path

README_PATH = Path(__file__).resolve().parent.parent / "task6_read_me.txt"


def count_words(path=README_PATH):
    """Return the number of whitespace-separated words in the file at path."""
    with open(path, "r") as f:
        text = f.read()
    return len(text.split())


if __name__ == "__main__":
    print(count_words())
