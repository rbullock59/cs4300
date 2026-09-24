"""Task 5: lists and dictionaries."""

books = [
    ("Dune", "Frank Herbert"),
    ("Neuromancer", "William Gibson"),
    ("The Hobbit", "J.R.R. Tolkien"),
    ("Snow Crash", "Neal Stephenson"),
    ("1984", "George Orwell"),
]

students = {
    "Alice": "S1001",
    "Bob": "S1002",
    "Carol": "S1003",
}


def first_three_books():
    return books[:3]


def get_student_id(name):
    return students.get(name)


if __name__ == "__main__":
    print(first_three_books())
    print(students)
