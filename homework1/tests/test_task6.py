from src.task6 import count_words, README_PATH


def test_count_words_readme():
    assert count_words(README_PATH) == 104


def test_count_words_simple(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("one two three four")
    assert count_words(f) == 4


def test_count_words_empty_file(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("")
    assert count_words(f) == 0
