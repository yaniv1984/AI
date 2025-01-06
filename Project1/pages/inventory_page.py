from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.inventory_items = ".inventory_item"
        self.add_to_cart_button = '[data-test="add-to-cart-sauce-labs-backpack"]'
        self.cart_badge = ".shopping_cart_badge"

    def get_inventory_count(self):
        return self.page.locator(self.inventory_items).count()

    def add_first_item_to_cart(self):
        self.click(self.add_to_cart_button)

    def get_cart_badge_count(self):
        return self.get_text(self.cart_badge)
