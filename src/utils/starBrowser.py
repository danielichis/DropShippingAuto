from playwright.sync_api import sync_playwright
from playwright.sync_api import Page,Expect
def start_browser():
    print("iniciando navegador...")
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context=browser.new_context(storage_state="src/sessions/state_amazon.json")
    page = context.new_page()
    print("Navegador prendido...")
    return page
if __name__ == '__main__':
    start_browser()