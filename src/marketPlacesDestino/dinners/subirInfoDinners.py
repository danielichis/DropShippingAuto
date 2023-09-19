from playwright.sync_api import sync_playwright
from src.utils.dinamySelections import search_best_option
import time
homeDinners="https://admin.quickcomm.co/catalog/products"
import re

with sync_playwright() as p:
    user_dir=r"C:\Users\Daniel\AppData\Local\Google\Chrome\User Data2"
    browser = p.chromium.launch_persistent_context(user_dir,headless=False)
    page_DIN=browser.new_page()
    page_DIN.goto(homeDinners)
    
    page_DIN.get_by_role("button", name=" Crear Producto").click()
    page_DIN.get_by_role("button", name=" Empezar").click()
    
    page_DIN.locator("//span[text()='Vendedor']//parent::div//input").click()
    page_DIN.locator("//a[text()='UNALUKA INTERNACIONAL']").click()

    marca_a_buscar="AMAZON"
    page_DIN.locator("//span[text()='Marca']//parent::div//input").type(marca_a_buscar,delay=100)
    lista_marcas=page_DIN.locator("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
    best_option=search_best_option(marca_a_buscar,lista_marcas,"-")
    page_DIN.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()

    categoria="PARLANTE"
    page_DIN.locator("//span[text()='Categoría']//parent::div//input").type(categoria,delay=100)
    lista_categorias=page_DIN.locator("//span[text()='Categoría']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
    best_option=search_best_option(categoria,lista_categorias,"-")
    page_DIN.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()

    page_DIN.locator("div").filter(has_text=re.compile(r"^Código InternoIdentificador unico \(Opcional\)$")).get_by_role("textbox").fill("555555")
    
    page_DIN.locator("div").filter(has_text=re.compile(r"^Nombre Producto$")).get_by_role("textbox").fill("Nuevo Echo Dot con reloj (5.ª generación, modelo de 2022) | versión internacional con adaptador de corriente (15 W)")

    page_DIN.locator("//div[@class='ngx-editor-textarea']").fill("ahora si probando con el div")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Precio Base$")).get_by_role("spinbutton").fill("20")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Precio Especial$")).get_by_role("spinbutton").fill("15")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Puntos$")).get_by_role("spinbutton").fill("15")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Costo por artículo$")).get_by_role("spinbutton").fill("15")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Margen$")).get_by_role("textbox").fill("25%")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Ganancia$")).get_by_role("textbox").fill("5")
    page_DIN.locator("div").filter(has_text=re.compile(r"^SKU \(código de artículo\)$")).get_by_role("textbox").fill("999999")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Código de barras \(ISBN, UPC, GTIN, etc\.\)$")).get_by_role("textbox").fill("888888888888888")
    page_DIN.locator("div").filter(has_text=re.compile(r"^Stock$")).get_by_role("spinbutton").fill("1")
    page_DIN.get_by_placeholder("Largo cm").fill("15")
    page_DIN.get_by_placeholder("Ancho cm").fill("15")
    page_DIN.get_by_placeholder("Altura cm").fill("15")
    page_DIN.get_by_placeholder("Peso").fill("300")

    lista_atributos_adicionales=page_DIN.locator("//div[@class='col-md-6 ng-star-inserted']//span[text()='*']/parent::span").all_inner_texts()
    page_DIN.pause()
    print("hola mochi")

    
