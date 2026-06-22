import re


def contains_sql_injection_pattern(user_input):
    """
    Extra SQL injection detection layer for demo/security monitoring.
    SQLAlchemy ORM remains the main protection against SQL injection.
    """

    if not user_input:
        return False

    text = user_input.lower()

    # Block quote characters used in common SQL injection attempts
    if "'" in text or '"' in text:
        return True

    suspicious_words = [
        "select",
        "insert",
        "update",
        "delete",
        "drop",
        "union",
        " or ",
        " and ",
        "--",
        ";",
        "/*",
        "*/"
    ]

    for word in suspicious_words:
        if word in text:
            return True

    return False


def is_valid_username(username):
    """
    Username allows only letters, numbers, dots, and underscores.
    """

    return bool(re.fullmatch(r"[A-Za-z0-9_.]{3,30}", username))