from app.cv_checker import check_cv

def test_check_cv():
    text = """
    Name: Alex Smith
    Email: alex@example.com
    Skills: Python, FastAPI, SQL
    """

    result = check_cv(text)
    assert result["name"] == True
    assert result["email"] == True
    assert result["skills"] == True