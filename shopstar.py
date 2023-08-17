#import playwright
from playwright.sync_api import sync_playwright

homeShopstarUrl="https://sellers.shopstar.pe/"
homeMercadoLibre="https://www.mercadolibre.com.pe/"
homeRealPlaza="https://inretail.mysellercenter.com"

with sync_playwright() as p:
    user_dir=r"C:\Users\Daniel\AppData\Local\Google\Chrome\User Data2"
    browser = p.chromium.launch_persistent_context(user_dir, headless=False)
    #pageRL = browser.new_page()
    #pageRL.goto(homeRealPlaza)
    pageML=browser.new_page()
    pageML.goto(homeMercadoLibre)
    pageML.get_by_role("link", name="Publicaciones").click()
    pageML.get_by_role("button", name="Publicar").click()
    pageML.get_by_role("link", name="De forma individual").click()
    pageML.get_by_role("button", name="Iniciar nueva publicación").click()
    #pageSP=browser.new_page()
    #pageSP.goto(homeShopstarUrl)
    pageML.pause()
    pageML.quit()
    

