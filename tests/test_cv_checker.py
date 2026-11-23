from app.cv_checker import check_cv


def test_english_cv():
    text = """Alex Smith
alex@example.com
+46 767 010 985
Experience
Backend Developer at Example AB
Education
Computer Science
Skills
Python, FastAPI, Docker
"""
    result = check_cv(text)

    assert all(item["found"] for item in result.values())
    assert result["name"]["value"] == "Alex Smith"
    assert result["email"]["value"] == "alex@example.com"
    assert result["phone"]["value"] == "+46 767 010 985"
    assert "Backend Developer" in result["experience"]["value"]
    assert "Computer Science" in result["education"]["value"]
    assert "Docker" in result["skills"]["value"]


def test_swedish_cv():
    text = """MOHAMMAD REZA HEYDARI
DevOps-student
Stockholm · +46 767 010 985 · example@nackademin.se
PROFIL
Student
ARBETSLIVSERFARENHET
Automationsguiden AB | Backendutveckling och DevOps
UTBILDNING
Nackademin | DevOps Engineer
UTVALDA PRAKTISKA PROJEKT
Azure och resurshantering
TEKNISKA KUNSKAPER
Linux, Python, Docker, Git
SPRÅK OCH REFERENS
Svenska och engelska
"""
    result = check_cv(text)

    assert all(item["found"] for item in result.values())
    assert result["name"]["value"] == "MOHAMMAD REZA HEYDARI"
    assert "Automationsguiden" in result["experience"]["value"]
    assert "Nackademin" in result["education"]["value"]
    assert "Docker" in result["skills"]["value"]
    assert "SPRÅK" not in result["skills"]["value"]


def test_missing_fields():
    result = check_cv("PROFIL\\nLooking for a job.")
    assert all(not item["found"] for item in result.values())


def test_keywords_alone_are_not_values():
    result = check_cv("Name\\nEmail\\nPhone\\nSkills")
    assert not result["name"]["found"]
    assert not result["email"]["found"]
    assert not result["phone"]["found"]
    assert not result["skills"]["found"]
