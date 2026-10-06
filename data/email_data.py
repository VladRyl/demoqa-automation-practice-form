VALID_EMAILS = [
    "simple@example.com",
    "very.common@example.com",
    "disposable.style.email.with+symbol@example.com",
    "other.email-with-hyphen@example.com",
    "fully-qualified-domain@example.co.uk",
    "user.name+tag+sorting@example.com",
    "x@example.com",
    "example-indeed@strange-example.com",
]

INVALID_EMAILS = [
    "plainaddress",
    "#@%^%#$@#$@#.com",
    "@example.com",
    "Joe Smith <email@example.com>",
    "email.example.com",
    "email@example@example.com",
    ".email@example.com",
    "email.@example.com",
    "email..email@example.com",
    "email@example.com (Joe Smith)",
    "email@example",
    "email@-example.com",
    "email@example..com",
    "Abc..123@example.com",
    "admin@mailserver1",
]
