"""
Learn the basic fixture pattern:
create reusable setup data once, then request it by name in multiple tests.

Common PyTest fixture scopes:
- function: run once per test function (default)
- class: run once per test class
- module: run once per test file/module
- package: run once per Python package
- session: run once for the whole PyTest run
"""

import pytest


@pytest.fixture
def sample_user():
    print("\nFIXTURE: creating sample user")
    user = {
        "id": 1,
        "name": "Admas",
        "role": "student",
    }
    yield user
    print("\nFIXTURE: cleaning up sample user")


def test_1_user_has_name_1(sample_user):
    print("TEST 1: checking the user's name")
    assert sample_user["name"] == "Admas"



def test_1_user_has_role(sample_user):
    print("TEST 2: checking the user's role")
    assert sample_user["role"] == "student"


def test_1_user_has_id_(sample_user):
    print("TEST 3: checking the user's id")
    assert sample_user["id"] == 1
