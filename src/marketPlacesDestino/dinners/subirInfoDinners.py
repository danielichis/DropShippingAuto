from playwright.sync_api import sync_playwright
from DropShippingAuto.src.utils.dinamySelections import search_best_option
from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
import json
import time
homeDinners="https://admin.quickcomm.co/catalog/products"
import re



class multiLoaderDinners:
    def __init__(self,dataToLoad):
        self.dataToLoad=dataToLoad
        self.p = sync_playwright().start()
        user_dir=r"C:\Users\Daniel\AppData\Local\Google\Chrome\User Data2"
        self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False)
        self.page=self.browser.new_page()
    
    def go_to_create_product(self):
        self.page.goto(homeDinners)
        self.page.get_by_role("button", name=" Crear Producto").click()
        self.page.get_by_role("button", name=" Empezar").click()

    def load_all_products(self):
        loadDinners=LoaderDinners(self.dataToLoad)
        for product in self.dataToLoad:
            self.load_main_dinners(product)

        
class LoaderDinners:
    def __init__(self,dataToLoad):
        self.dataToLoad=dataToLoad

    def load_seller(self):
        self.page.locator("//span[text()='Vendedor']//parent::div//input").click()
        self.page.locator("//a[text()='UNALUKA INTERNACIONAL']").click()

    def load_brand(self):
        marca_a_buscar=infoDinnersToLoad['data']['marca']
        self.page.locator("//span[text()='Marca']//parent::div//input").type(marca_a_buscar,delay=100)
        time.sleep(0.5)
        self.page.wait_for_selector("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']")
        lista_marcas=self.page.locator("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
        best_option=search_best_option(marca_a_buscar,lista_marcas,"-")
        self.page.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()

    def load_category(self):
        categoria=infoDinnersToLoad['data']['categoria']
        categoria.reverse()
        for cate in categoria:
            self.page.locator("//span[text()='Categoría']//parent::div//input").type(cate,delay=100)
            lista_categorias=self.page.locator("//span[text()='Categoría']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
            if len(lista_categorias)>0:
                best_option=search_best_option(cate,lista_categorias,"-")
                self.page.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()
                break
            else:
                self.page.locator("//span[text()='Categoría']//parent::div//input").fill("")

    def load_upc(self):
        upc=get_upc(infoDinnersToLoad['data']['sku'])
        self.page.locator("div").filter(has_text=re.compile(r"^Código InternoIdentificador unico \(Opcional\)$")).get_by_role("textbox").fill(upc)
        self.page.query_selector("input[formcontrolname='barCode']").fill(upc)

    def load_name_product(self):
        name_product=infoDinnersToLoad['data']['nombreProducto']
        self.page.locator("div").filter(has_text=re.compile(r"^Nombre Producto$")).get_by_role("textbox").fill(name_product)

    def load_description(self):
        description=infoDinnersToLoad['data']['descripcion']
        self.page.locator("//div[@class='ngx-editor-textarea']").fill(description)

    def load_base_price(self):
        base_price=infoDinnersToLoad['data']['precioBase'] 
        base_price=str(round(float(re.findall(r"(\d+\.\d+)",base_price)[0]),2))
        self.page.locator("div").filter(has_text=re.compile(r"^Precio Base$")).get_by_role("spinbutton").fill(base_price)

    def load_special_price(self):
        special_price=infoDinnersToLoad['data']['precioBase']
        special_price=str(round(float(re.findall(r"(\d+\.\d+)",special_price)[0]),2))
        self.page.locator("div").filter(has_text=re.compile(r"^Precio Especial$")).get_by_role("spinbutton").fill(special_price)

    def load_price_factors(self):
        points="15"
        article_cost="15"
        margin="25%"
        profit="5"
        self.page.locator("div").filter(has_text=re.compile(r"^Puntos$")).get_by_role("spinbutton").fill(points)
        self.page.locator("div").filter(has_text=re.compile(r"^Costo por artículo$")).get_by_role("spinbutton").fill(article_cost)
        self.page.locator("div").filter(has_text=re.compile(r"^Margen$")).get_by_role("textbox").fill(margin)
        self.page.locator("div").filter(has_text=re.compile(r"^Ganancia$")).get_by_role("textbox").fill(profit)

    def load_sku(self):
        sku=infoDinnersToLoad['data']['sku']
        self.page.locator("div").filter(has_text=re.compile(r"^SKU \(código de artículo\)$")).get_by_role("textbox").fill(sku)
    def load_stock(self):
        stock="1"
        self.page.locator("div").filter(has_text=re.compile(r"^Stock$")).get_by_role("spinbutton").fill(stock)

    def load_dimensions(self):
        dimensions=infoDinnersToLoad['data']['dimensions_cm']
        self.page.get_by_placeholder("Largo cm").fill(str(dimensions["Largo cm"]))
        self.page.get_by_placeholder("Ancho cm").fill(str(dimensions["Ancho cm"]))
        self.page.get_by_placeholder("Altura cm").fill(str(dimensions["Altura cm"]))
        self.page.get_by_placeholder("Peso").fill(dimensions["peso_kg"])

    def load_images(self):
        for imagePath in infoDinnersToLoad["imagesPath"]:
            self.page.locator(".uploaded-photos__item > input").first.set_input_files(imagePath)

    def load_aditional_fields(self):
        self.page.wait_for_selector("div[class='col-md-6 ng-star-inserted']")
        aditionalFields=self.page.query_selector_all("div[class='col-md-6 ng-star-inserted']")
        lista_atributos_adicionales=self.page.locator("//div[@class='col-md-6 ng-star-inserted']//span[text()='*']/parent::span").all_inner_texts()
        lista_obligatorios=self.page.query_selector("div[class='col-md-6 ng-star-inserted'] div span[class='ng-star-inserted']")
        lista_inputs=self.page.query_selector("div[class='col-md-6 ng-star-inserted'] div input")
        lista_selects=self.page.query_selector("div[class='col-md-6 ng-star-inserted'] div select")
        lista_opcionales=self.page.query_selector("div[class='col-md-6 ng-star-inserted'] div>span:not(:has(>span))")
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

    def load_main_dinners(self):
        self.load_images()
        self.load_seller()
        self.load_category()
        self.load_brand()
        self.load_name_product()
        self.load_description()
        self.load_base_price()
        self.load_special_price()
        self.load_sku()
        self.load_upc()
        self.load_dimensions()
        self.load_aditional_fields()
if __name__ == "__main__":
    mloader=multiLoaderDinners(infoDinnersToLoad)
    mloader.go_to_create_product()

    
