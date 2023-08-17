from playwright import sync_playwright

class Actor:
    def __init__(self, page):
        self.page = page

    def perform_as(self, task):
        task.perform_as(self)

class Task1:
    def __init__(self, actor):
        self.actor = actor

    def login(self):
        self.actor.page.goto("https://example.com/login")
        self.actor.page.fill("username", "johndoe")
        self.actor.page.fill("password", "secret")
        self.actor.page.click("Login")

class Task2:
    def __init__(self, actor):
        self.actor = actor

    def place_order(self):
        self.actor.page.goto("https://example.com/cart")
        self.actor.page.click("Add to cart")
        self.actor.page.click("Checkout")
        self.actor.page.fill("name", "John Doe")
        self.actor.page.fill("address", "123 Main Street")
        self.actor.page.fill("city", "Anytown")
        self.actor.page.fill("state", "CA")
        self.actor.page.fill("zip code", "91234")
        self.actor.page.fill("phone number", "123-456-7890")
        self.actor.page.click("Place Order")

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page()
    actor = Actor(page)
    task1 = Task1(actor)
    task2 = Task2(actor)
    task1.login()
    task2.place_order()
    browser.close()