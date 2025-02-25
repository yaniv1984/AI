import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.saucedemo.com/"

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        yield page
        browser.close()

