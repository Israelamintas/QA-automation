"""
Shared fixtures for the fixture examples.
"""

import pytest


@pytest.fixture(scope="session")
def session_user():
    print("\nSESSION-SCOPE FIXTURE: creating sample user")
    user = {
        "id": 100,
        "name": "Session User",
        "role": "shared",
    }
    yield user
    print("\nSESSION-SCOPE FIXTURE: cleaning up sample user")
