import pytest
from _pytest.mark import param

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
BASE_URL = "https://www.saucedemo.com/"


@pytest.fixture(scope="session")
def some_function_name():
    print("this is setup")
    yield
    print("this is teardown")

def test_inventory_items_load(browser):
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    # Login
    login_page.goto(BASE_URL)
    login_page.login("standard_user", "secret_sauce")

    # Verify inventory items
    assert inventory_page.get_inventory_count() > 0

def test_add_to_cart(browser):
    login_page = LoginPage(browser)
    inventory_page = InventoryPage(browser)

    # Login
    login_page.goto(BASE_URL)
    login_page.login("standard_user", "secret_sauce")

    # Add item to cart
    inventory_page.add_first_item_to_cart()
    assert inventory_page.get_cart_badge_count() == "1"
