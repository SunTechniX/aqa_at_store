import json
from playwright.sync_api import sync_playwright, expect


# https://automationteststore.com/index.php?rt=r/product/product/addToCart
# {
#     "cart_details": "\t<div class=\"empty_cart text-center\">\n\t\t<i class=\"fa fa-shopping-cart\"><\/i>\n\t<\/div>\n",
#     "item_count": 0,
#     "total": "0.00\u20ac"
# }

def test_at_store_01():
    def handle_route(route):
        if route.request.resource_type in ("image", "stylesheet"):
            route.abort()
        else:
            # print(f">>> Запрос: {route.request.url}")
            route.continue_()  # Продолжить как есть

    def handle_product(route):
        print(f"\n#### Запрос: {route.request.url}")
        response = route.fetch()
        # print(f"{response=}")
        # print(f"{response.json()=}")
        data = response.json()
        print(f"{data['total']=}")
        if "€" in data['total']:
            data['total'] = data['total'].replace("€", "RU")
            route.fulfill(json=data)
            print("Подменил запрос")
        else:
            route.continue_()  # Продолжить как есть


    with sync_playwright() as drv:
        browser = drv.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_timeout(6_000)
        page.pause()

        # page.route("**/*", handle_route)
        page.route("**/*/addToCart*", handle_product)

        page.goto("https://automationteststore.com/")
        page.locator("a").filter(has_text="$ US Dollar").first.click()
        page.get_by_role("link", name="€ Euro").click()

        page.wait_for_timeout(2_000)
        page.pause()
        # ---------------------
        context.close()
        browser.close()
