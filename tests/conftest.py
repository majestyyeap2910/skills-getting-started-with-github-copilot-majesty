"""Shared pytest fixtures for the backend API tests."""

import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    """Provide a FastAPI TestClient for making requests to the app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the in-memory activities before/after each test.

    The app stores activities in a module-level dict, so tests that mutate it
    (signup/unregister) would leak state into other tests. We deep-copy the
    original data, let the test run, then restore it to keep tests isolated.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
