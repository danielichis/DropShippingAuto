from playwright.sync_api import Page,Expect

def got_to_amazon(page:Page):
    page.goto("https://www.amazon.com/")
