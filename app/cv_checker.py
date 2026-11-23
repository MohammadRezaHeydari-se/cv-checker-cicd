import re


HEADINGS = {
    "experience": (
        "experience", "work experience", "employment history",
        "arbetslivserfarenhet", "arbetslivserfarenheter",
    ),
    "education": ("education", "utbildning", "utbildningar"),
    "skills": (
        "skills", "technical skills", "competencies",
        "tekniska kunskaper", "kompetenser", "färdigheter",
    ),
}

OTHER_HEADINGS = {
    "profile", "summary", "profil", "sammanfattning",
    "projects", "selected projects", "utvalda praktiska projekt",
    "languages", "references", "språk och referens",
    "certifications", "certifikat", "contact", "kontakt",
}


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().casefold().rstrip(":")


def extract_sections(lines: list[str]) -> dict[str, str | None]:
    results = {key: None for key in HEADINGS}
    known = {
        normalize(heading): key
        for key, headings in HEADINGS.items()
        for heading in headings
    }

    current = None
    collected = []

    def save():
        if current and collected:
            value = " ".join(collected).strip()
            if value:
                results[current] = value[:700]

    for line in lines:
        heading = normalize(line)

        if heading in known or heading in OTHER_HEADINGS:
            save()
            current = known.get(heading)
            collected = []
            continue

        inline = re.match(r"^([^:]{2,40}):\s*(.+)$", line)
        if inline and normalize(inline.group(1)) in known:
            save()
            current = known[normalize(inline.group(1))]
            collected = [inline.group(2)]
            continue

        if current:
            collected.append(line)

    save()
    return results


def check_cv(text: str) -> dict:
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )
    email = email_match.group(0) if email_match else None

    phone = None
    phone_pattern = (
        r"(?<![\w+])(?:\+\d{1,3}[\s.-]*)?"
        r"(?:\d[\s.-]*){7,14}\d(?!\w)"
    )

    for match in re.finditer(phone_pattern, text):
        candidate = match.group(0).strip()
        digits = re.sub(r"\D", "", candidate)

        if 8 <= len(digits) <= 15 and (
            candidate.startswith("+") or candidate.startswith("0")
        ):
            phone = candidate
            break

    name = None
    if lines:
        first = re.sub(r"^name\s*:\s*", "", lines[0], flags=re.I).strip()
        words = first.split()

        if (
            2 <= len(words) <= 5
            and all(
                re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ'-]+", word)
                for word in words
            )
            and normalize(first) not in OTHER_HEADINGS
        ):
            name = first

    sections = extract_sections(lines)
    values = {"name": name, "email": email, "phone": phone, **sections}

    return {
        key: {"found": bool(value), "value": value}
        for key, value in values.items()
    }
