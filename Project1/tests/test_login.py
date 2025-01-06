from pages.login_page import LoginPage

BASE_URL = "https://www.saucedemo.com/"

def test_login_valid_credentials(browser):
    login_page = LoginPage(browser)
    login_page.goto(BASE_URL)
    login_page.login("standard_user", "secret_sauce")
    assert browser.url == f"{BASE_URL}inventory.html"

def test_login_invalid_credentials(browser):
    login_page = LoginPage(browser)
    login_page.goto(BASE_URL)
    login_page.login("invalid_user", "wrong_password")
    assert login_page.get_error_message() == "Epic sadface: Username and password do not match any user in this service"
