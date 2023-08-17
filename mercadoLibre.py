#import playwright
from playwright.sync_api import sync_playwright
import re
homeShopstarUrl="https://sellers.shopstar.pe/"
homeMercadoLibre="https://www.mercadolibre.com.pe/"
homeRealPlaza="https://inretail.mysellercenter.com"

with sync_playwright() as p:
    user_dir=r"C:\Users\Daniel\AppData\Local\Google\Chrome\User Data2"
    browser = p.chromium.launch_persistent_context(user_dir, headless=False)
    #pageRL = browser.new_page()
    #pageRL.goto(homeRealPlaza)
    pageML=browser.new_page()
    #pageML.goto(homeMercadoLibre)
    #pageML.goto("https://myaccount.mercadolibre.com.pe/listings/list#menu-user")
    #pageML.goto("https://www.mercadolibre.com.pe/publicar#from=listings")
    pageML.goto("https://www.mercadolibre.com.pe/publicar/hub")

    #pageML.get_by_role("link", name="Publicaciones").click()
    #pageML.get_by_role("button", name="Publicar").click()
    #pageML.get_by_role("link", name="De forma individual").click()
    #pageML.wait_for_selector("button:has-text('Iniciar nueva publicación')")
    #pageML.locator("//a[contains(text(),'Iniciar nueva publicación')]").click()
    #pageML.get_by_role("button", name="Iniciar nueva publicación").click()
    

    pageML.locator("div").filter(has_text=re.compile(r"^Productos$")).nth(1).click()
    pageML.get_by_placeholder("Ej.: Celular Samsung Galaxy S9 64 GB Negro o 887276246529").click()
    pageML.get_by_placeholder("Ej.: Celular Samsung Galaxy S9 64 GB Negro o 887276246529").fill("productonametest")
    pageML.get_by_role("button", name="Comenzar").click()
    pageML.get_by_role("link", name="Es de otra categoría").click()
    pageML.locator("li").filter(has_text="Celulares y Teléfonos").click()
    pageML.locator("div").filter(has_text=re.compile(r"^Celulares y Smartphones$")).first.click()
    pageML.locator("div").filter(has_text=re.compile(r"^Apple$")).first.click()
    pageML.locator("#searchableOptionValuesContainer li").filter(has_text=re.compile(r"^Es Dual SIM$")).get_by_role("button").click()
    pageML.locator("div").filter(has_text=re.compile(r"^iPhone 13 mini 128gb$")).first.click()
    pageML.locator("li").filter(has_text="Otras capacidades").get_by_role("button").click()
    pageML.get_by_label("", exact=True).click()
    pageML.get_by_label("", exact=True).fill("8")
    pageML.locator("li").filter(has_text="GBGBGBkBkBMBMBTBTB").get_by_role("button").nth(3).click()
    pageML.get_by_role("button", name="Confirmar").click()
    pageML.locator("li").filter(has_text="Liberado").click()
    pageML.locator("#new").click()
    pageML.get_by_role("button", name="Elegir Color").click()
    pageML.get_by_role("button", name="Elegir Color").click()
    pageML.get_by_role("button", name="Negro").click()
    pageML.get_by_role("button", name="Confirmar").click()
    pageML.get_by_placeholder("Ej: Celular Samsung Galaxy S9 64 GB negro").click()
    pageML.get_by_placeholder("Ej: Celular Samsung Galaxy S9 64 GB negro").click()
    pageML.get_by_placeholder("Ej: Celular Samsung Galaxy S9 64 GB negro").click()
    pageML.get_by_placeholder("Ej: Celular Samsung Galaxy S9 64 GB negro").click(click_count=3)
    pageML.get_by_placeholder("Ej: Celular Samsung Galaxy S9 64 GB negro").fill("descripcion de prueba para celular")
    pageML.get_by_role("button", name="Continuar").click()
    pageML.locator("label").filter(has_text="Mi producto no lo tiene").locator("span").nth(1).click()
    pageML.get_by_role("button", name="¿Por qué no lo tiene?").click()
    pageML.get_by_test_id("dont-have-17055159-id").locator("div").nth(1).click()
    pageML.get_by_role("button", name="Confirmar").nth(1).click()

    # --------------------
    browser.close()
    #pageSP=browser.new_page()
    #pageSP.goto(homeShopstarUrl)
    pageML.pause()
    pageML.quit()
    

