def check_cv(text: str) -> dict:
    test = text.lower()

    sections = [
        "name",
        "email",
        "phone",
        "experience",
        "education",
        "skills",
    ]

    results = {}

    for section in sections:
        results[section] = section in test

    return results
