from src.task5 import books, students, first_three_books, get_student_id


def test_first_three_books():
    assert first_three_books() == books[:3]
    assert len(first_three_books()) == 3


def test_books_are_title_author_pairs():
    assert all(len(b) == 2 for b in books)


def test_student_lookup():
    assert get_student_id("Alice") == "S1001"


def test_student_lookup_missing():
    assert get_student_id("Nobody") is None


def test_students_dict_shape():
    assert isinstance(students, dict)
    assert len(students) == 3
