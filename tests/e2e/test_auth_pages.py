"""
Playwright E2E tests for the login/register front-end pages: client-side
validation, JWT storage in localStorage, and server-driven error states.
"""
import re
import pytest
import requests
from playwright.sync_api import Page, expect

from tests.conftest import create_fake_user

STRONG_PASSWORD = "TestPass123!"  # satisfies backend UserCreate validator
                                   # (upper/lower/digit/special char, 8-128 chars)


def _register_via_api(base_url: str, **overrides) -> dict:
    """
    Fast setup helper: register a real user directly via the JSON API,
    bypassing the UI, for tests that only need a pre-existing account
    (e.g. login-flow tests).
    """
    user = create_fake_user()
    user["password"] = STRONG_PASSWORD
    user.update(overrides)
    payload = {**user, "confirm_password": STRONG_PASSWORD}
    resp = requests.post(f"{base_url.rstrip('/')}/register", json=payload)
    assert resp.status_code == 201, resp.text
    return user


@pytest.mark.e2e
def test_register_form_valid_data_shows_success(page: Page, fastapi_server: str):
    """Drives the actual register.html form end-to-end with valid, strong
    Faker-backed data and confirms the success alert renders."""
    user = create_fake_user()

    page.goto(f"{fastapi_server}register")

    page.locator("#username").fill(user["username"])
    page.locator("#email").fill(user["email"])
    page.locator("#first_name").fill(user["first_name"])
    page.locator("#last_name").fill(user["last_name"])
    page.locator("#password").fill(STRONG_PASSWORD)
    page.locator("#confirm_password").fill(STRONG_PASSWORD)

    page.locator("#registrationForm button[type='submit']").click()

    expect(page.locator("#successAlert")).to_be_visible()
    expect(page.locator("#successMessage")).to_contain_text("Registration successful")


@pytest.mark.e2e
def test_login_form_correct_credentials_stores_token(page: Page, fastapi_server: str):
    """Pre-registers a user via the API (fast setup), then drives the actual
    login.html form and confirms both the success alert and localStorage."""
    user = _register_via_api(fastapi_server)

    page.goto(f"{fastapi_server}login")
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill(STRONG_PASSWORD)
    page.locator("#loginForm button[type='submit']").click()

    expect(page.locator("#successAlert")).to_be_visible()
    expect(page.locator("#successMessage")).to_contain_text("Login successful")

    access_token = page.evaluate("() => localStorage.getItem('access_token')")
    assert access_token, "access_token was not stored in localStorage"

    # Confirm the redirect to /dashboard actually fires afterward.
    expect(page).to_have_url(re.compile(r".*/dashboard$"), timeout=5000)


@pytest.mark.e2e
def test_register_form_weak_password_blocked_client_side(page: Page, fastapi_server: str):
    """Client-side validation must reject a short password before any
    network round-trip -- no fetch is made, DOM error state only."""
    user = create_fake_user()

    page.goto(f"{fastapi_server}register")
    page.locator("#username").fill(user["username"])
    page.locator("#email").fill(user["email"])
    page.locator("#first_name").fill(user["first_name"])
    page.locator("#last_name").fill(user["last_name"])
    page.locator("#password").fill("short1")          # < 8 chars
    page.locator("#confirm_password").fill("short1")

    page.locator("#registrationForm button[type='submit']").click()

    expect(page.locator("#errorAlert")).to_be_visible()
    expect(page.locator("#errorMessage")).to_contain_text("at least 8 characters")
    expect(page).to_have_url(re.compile(r".*/register$"))


@pytest.mark.e2e
def test_login_form_wrong_password_shows_error(page: Page, fastapi_server: str):
    """Server-side 401 on a wrong password must surface as a UI error."""
    user = _register_via_api(fastapi_server)

    page.goto(f"{fastapi_server}login")
    page.locator("#username").fill(user["username"])
    page.locator("#password").fill("TotallyWrongPass1!")
    page.locator("#loginForm button[type='submit']").click()

    expect(page.locator("#errorAlert")).to_be_visible()
    expect(page.locator("#errorMessage")).to_contain_text("Invalid username or password")
    expect(page).to_have_url(re.compile(r".*/login$"))
