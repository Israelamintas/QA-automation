"""
Learn that scope="module" runs once per module, so this second file gets its own fixture run.
"""

import pytest


@pytest.fixture(scope="module")
def sample_user():
    print("\nMODULE-SCOPE FIXTURE PART 2: creating sample user")
    user = {
        "id": 2,
        "name": "Alex",
        "role": "admin",
    }
    yield user
    print("\nMODULE-SCOPE FIXTURE PART 2: cleaning up sample user")


def test_scope_module_part_2_user_has_name(sample_user):
    print("PART 2 - TEST 1: checking the user's name")
    assert sample_user["name"] == "Alex"


def test_scope_module_part_2_user_has_role(sample_user):
    print("PART 2 - TEST 2: checking the user's role")
    assert sample_user["role"] == "admin"


def test_scope_module_part_2_user_has_id(sample_user):
    print("PART 2 - TEST 3: checking the user's id")
    assert sample_user["id"] == 2
