from playwright.sync_api import async_playwright
from playwright.sync_api import Page,Expect
def start_browser():
    print("iniciando navegador...")
    p = async_playwright().start()
    browser = p.chromium.launch(headless=False)
    context=browser.new_context(storage_state="src/sessions/state_amazon.json")
    page = context.new_page()
    print("Navegador prendido...")
    return page
