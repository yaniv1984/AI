from playwright.sync_api import sync_playwright
import pytest

BASE_URL = "https://www.saucedemo.com/"


@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        yield page
        browser.close()


# Test: Login with valid credentials
def test_login_valid_credentials(browser):
    browser.goto(BASE_URL)

    # Fill in login form
    browser.fill("#user-name", "standard_user")
    browser.fill("#password", "secret_sauce")
    browser.click("#login-button")

    # Assert successful login
    assert browser.url == f"{BASE_URL}inventory.html"


# Test: Login with invalid credentials
def test_login_invalid_credentials(browser):
    browser.goto(BASE_URL)

    # Fill in login form with incorrect credentials
    browser.fill("#user-name", "invalid_user")
    browser.fill("#password", "wrong_password")
    browser.click("#login-button")

    # Assert error message is displayed
    error_message = browser.locator('[data-test="error"]')
    assert error_message.text_content() == "Epic sadface: Username and password do not match any user in this service"


# Test: Inventory items load correctly
def test_inventory_items_load(browser):
    browser.goto(BASE_URL)

    # Login
    browser.fill("#user-name", "standard_user")
    browser.fill("#password", "secret_sauce")
    browser.click("#login-button")

    # Verify inventory items are loaded
    items = browser.locator(".inventory_item")
    assert items.count() > 0


# Test: Add item to cart
def test_add_to_cart(browser):
    browser.goto(BASE_URL)

    # Login
    browser.fill("#user-name", "standard_user")
    browser.fill("#password", "secret_sauce")
    browser.click("#login-button")

    # Add the first item to the cart
    browser.locator(".inventory_item button").nth(0).click()

    # Verify cart badge is updated
    cart_badge = browser.locator(".shopping_cart_badge")
    assert cart_badge.text_content() == "1"


# Test: Complete checkout process
def test_checkout_process(browser):
    browser.goto(BASE_URL)

    # Login
    browser.fill("#user-name", "standard_user")
    browser.fill("#password", "secret_sauce")
    browser.click("#login-button")

    # Add item to the cart
    browser.click(".inventory_item button")

    # Go to cart page
    browser.click(".shopping_cart_link")
    assert browser.url == f"{BASE_URL}cart.html"
    assert browser.url == f"{BASE_URL}cart.html"

    # Proceed to checkout
    browser.click("#checkout")
    browser.fill("#first-name", "John")
    browser.fill("#last-name", "Doe")
    browser.fill("#postal-code", "12345")
    browser.click("#continue")

    # Assert we are on the checkout overview page
    assert browser.url == f"{BASE_URL}checkout-step-two.html"
    browser.click("#finish")

    # Verify order completion
    success_message = browser.locator(".complete-header")
    assert success_message.text_content() == "Thank you for your order"
