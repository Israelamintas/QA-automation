"""
Learn fixture scope="session": this fixture comes from conftest.py and runs once for the whole test run.
"""


def test_scope_session_user_has_name(session_user):
    print("PART 1 - TEST 1: checking the session user's name")
    assert session_user["name"] == "Session User"


def test_scope_session_user_has_role(session_user):
    print("PART 1 - TEST 2: checking the session user's role")
    assert session_user["role"] == "shared"


def test_scope_session_user_has_id(session_user):
    print("PART 1 - TEST 3: checking the session user's id")
    assert session_user["id"] == 100
