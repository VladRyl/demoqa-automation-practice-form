VALID_NAMES = [
    ("User", "Test"),
    ("A", "B"),
    ("John-Paul", "O'Connor"),
    ("Jean Luc", "Van Damme"),
    ("a" * 50, "b" * 50),
]

INVALID_NAMES = [
    ("", ""),
    ("User123", "Test"),
    ("User!", "Test#"),
    ("   ", "   "),
]
