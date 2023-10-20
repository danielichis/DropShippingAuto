from playwright.sync_api import sync_playwright
from src.utils.dinamySelections import search_best_option
from src.otrasWeb.scrapUpc import get_upc
from src.marketPlacesDestino.dinners.readAmazon import infoAmazon
import json
import time
homeDinners="https://admin.quickcomm.co/catalog/products"
import re


def go_to_create_product():
    page_DIN.goto(homeDinners)
    page_DIN.get_by_role("button", name=" Crear Producto").click()
    page_DIN.get_by_role("button", name=" Empezar").click()

def load_seller():
    page_DIN.locator("//span[text()='Vendedor']//parent::div//input").click()
    page_DIN.locator("//a[text()='UNALUKA INTERNACIONAL']").click()

def load_brand():
    marca_a_buscar=infoAmazon['data']['marca']
    page_DIN.locator("//span[text()='Marca']//parent::div//input").type(marca_a_buscar,delay=100)
    time.sleep(0.5)
    page_DIN.wait_for_selector("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']")
    lista_marcas=page_DIN.locator("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
    best_option=search_best_option(marca_a_buscar,lista_marcas,"-")
    page_DIN.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()

def load_category():
    categoria=infoAmazon['data']['categoria']
    categoria.reverse()
    for cate in categoria:
        page_DIN.locator("//span[text()='Categoría']//parent::div//input").type(cate,delay=100)
        lista_categorias=page_DIN.locator("//span[text()='Categoría']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
        if len(lista_categorias)>0:
            best_option=search_best_option(cate,lista_categorias,"-")
            page_DIN.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()
            break
        else:
            page_DIN.locator("//span[text()='Categoría']//parent::div//input").fill("")

def load_upc():
    upc=get_upc(infoAmazon['data']['sku'])
    page_DIN.locator("div").filter(has_text=re.compile(r"^Código InternoIdentificador unico \(Opcional\)$")).get_by_role("textbox").fill(upc)
    page_DIN.query_selector("input[formcontrolname='barCode']").fill(upc)

def load_name_product():
    name_product=infoAmazon['data']['nombreProducto']
    page_DIN.locator("div").filter(has_text=re.compile(r"^Nombre Producto$")).get_by_role("textbox").fill(name_product)

def load_description():
    description=infoAmazon['data']['descripcion']
    page_DIN.locator("//div[@class='ngx-editor-textarea']").fill(description)

def load_base_price():
    base_price=infoAmazon['data']['precioBase'] 
    base_price=str(round(float(re.findall(r"(\d+\.\d+)",base_price)[0]),2))
    page_DIN.locator("div").filter(has_text=re.compile(r"^Precio Base$")).get_by_role("spinbutton").fill(base_price)

def load_special_price():
    special_price=infoAmazon['data']['precioBase']
    special_price=str(round(float(re.findall(r"(\d+\.\d+)",special_price)[0]),2))
    page_DIN.locator("div").filter(has_text=re.compile(r"^Precio Especial$")).get_by_role("spinbutton").fill(special_price)

def load_price_factors():
    points="15"
    article_cost="15"
    margin="25%"
    profit="5"
    page_DIN.locator("div").filter(has_text=re.compile(r"^Puntos$")).get_by_role("spinbutton").fill(points)
    page_DIN.locator("div").filter(has_text=re.compile(r"^Costo por artículo$")).get_by_role("spinbutton").fill(article_cost)
    page_DIN.locator("div").filter(has_text=re.compile(r"^Margen$")).get_by_role("textbox").fill(margin)
    page_DIN.locator("div").filter(has_text=re.compile(r"^Ganancia$")).get_by_role("textbox").fill(profit)

def load_sku():
    sku=infoAmazon['data']['sku']
    page_DIN.locator("div").filter(has_text=re.compile(r"^SKU \(código de artículo\)$")).get_by_role("textbox").fill(sku)
def load_stock():
    stock="1"
    page_DIN.locator("div").filter(has_text=re.compile(r"^Stock$")).get_by_role("spinbutton").fill(stock)

def load_dimensions():
    dimensions=infoAmazon['data']['dimensions_cm']
    page_DIN.get_by_placeholder("Largo cm").fill(str(dimensions["Largo cm"]))
    page_DIN.get_by_placeholder("Ancho cm").fill(str(dimensions["Ancho cm"]))
    page_DIN.get_by_placeholder("Altura cm").fill(str(dimensions["Altura cm"]))
    page_DIN.get_by_placeholder("Peso").fill(dimensions["peso_kg"])

def load_images():
    for imagePath in infoAmazon["imagesPath"]:
        page_DIN.locator(".uploaded-photos__item > input").first.set_input_files(imagePath)

def load_aditional_fields():
    page_DIN.wait_for_selector("div[class='col-md-6 ng-star-inserted']")
    aditionalFields=page_DIN.query_selector_all("div[class='col-md-6 ng-star-inserted']")
    lista_atributos_adicionales=page_DIN.locator("//div[@class='col-md-6 ng-star-inserted']//span[text()='*']/parent::span").all_inner_texts()
    lista_obligatorios=page_DIN.query_selector("div[class='col-md-6 ng-star-inserted'] div span[class='ng-star-inserted']")
    lista_inputs=page_DIN.query_selector("div[class='col-md-6 ng-star-inserted'] div input")
    lista_selects=page_DIN.query_selector("div[class='col-md-6 ng-star-inserted'] div select")
    lista_opcionales=page_DIN.query_selector("div[class='col-md-6 ng-star-inserted'] div>span:not(:has(>span))")
    fieldsData=[]
    for field in aditionalFields:
        textField=field.query_selector("span").inner_text()
        if "*" in textField:
            mandatory=True
        else:
            mandatory=False
        numOfSelects=len(field.query_selector_all("select"))
        if numOfSelects>0:
            select=field.query_selector("select")
            options=options=[x.inner_text() for x in select.query_selector_all("option")]
            type="select"
        else:
            options=[]
            type="input"
        fieldData={
            "name":textField.replace("*","").strip(),
            "mandatory":mandatory,
            "options":options,
            "type":type
        }
        fieldsData.append(fieldData)
    
    with open("fieldsData.json", "w",encoding="utf-8") as f:
        json.dump(fieldsData, f, indent=4, ensure_ascii=False)
    print(fieldsData)


p = sync_playwright().start()
user_dir=r"C:\Users\Daniel\AppData\Local\Google\Chrome\User Data2"
browser = p.chromium.launch_persistent_context(user_dir,headless=False,record_video_dir="videos")
page_DIN=browser.new_page()
go_to_create_product()
load_images()
load_seller()
load_category()
load_brand()
load_name_product()
load_description()
load_base_price()
load_special_price()
load_sku()
load_upc()
load_dimensions()
load_aditional_fields()
#page_DIN.pause()


    
