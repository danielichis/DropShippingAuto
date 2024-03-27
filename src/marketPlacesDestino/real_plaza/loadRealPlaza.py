from playwright.sync_api import sync_playwright
from utils.jsHandler import insertPropertiesToPage
#from DropShippingAuto.src.utils.dinamySelections import search_best_option
#from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
#from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction
from utils.managePaths import mp
import json
import time
homeRealPlaza="https://inretail.mysellercenter.com/#/dashboard"
import re
from random import randrange


dataToLoad= [
        {
            "sku": "B07QSTJV95",
            "status_d": "descargado correctamente",
            "newProduct": "no",
            "product": {
                "estado": "Crear",
                "SKU": "B07QSTJV95",
                "PrecioShopify": "299.00",
                "PrecioListaShopify": "329",
                "PrecioDinners": "347",
                "PrecioRealPlaza": "347",
                "PrecioRipley": "347",
                "PrecioMercadoLibre": "369",
                "PrecioShopstar": "347",
                "fila": 85
            }
        },
        {
            "sku": "B0CKYF12ZR",
            "status_d": "descargado correctamente",
            "newProduct": "yes",
            "product": {
                "estado": "Crear",
                "SKU": "B0CKYF12ZR",
                "PrecioShopify": "149.00",
                "PrecioListaShopify": "164",
                "PrecioDinners": "175",
                "PrecioRealPlaza": "171",
                "PrecioRipley": "175",
                "PrecioMercadoLibre": "182",
                "PrecioShopstar": "171",
                "fila": 91
            }
        }
    ]


class multiLoaderRP:
    def __init__(self,dataToLoad):
        self.dataToLoad=dataToLoad
        self.p = sync_playwright().start()
        user_dir=r"C:\Users\risin\AppData\Local\Google\Chrome\UserData2"
        self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False)
        self.page=self.browser.new_page()
    
    def go_to_create_product(self):
        self.page.goto(homeRealPlaza)
        self.page.get_by_text("Catálogo").click()
        self.page.get_by_role("link", name="Administrar Productos").click()
        self.page.get_by_role("button", name="Crear Producto").click()
        print("pagina cargada")
        #self.page.get_by_role("button", name=" Crear Producto").click()
        #self.page.get_by_role("button", name=" Empezar").click()

    def load_product_name(self):
        #self.page.locator("input[id='nombreFormatterHelp']").fill("productName")
        self.page.get_by_role("textbox", name="Nombre").fill("productName")

    def load_description(self):
        #self.page.locator("input[id='nombreFormatterHelp']").fill("productName")
        properties={
                "name":"description1",
                "value":"23434"
            }
        insertPropertiesToPage("div[class='ql-editor ql-blank']",properties,self.page)
        print("Se insertó descripción")

    def load_category(self)->bool:
        #getting the list of categories
        #self.page.get_by_label("Categoría", exact=True).get_by_role("textbox").click()
        
        time.sleep(1)

        try:
            categoryListLocator=self.page.locator("div[class='list-group']>div[class='list-group-item']").all()
        except:
            print("Ya no hay más categorías por seleccionar")
            return False
            
        categoryList=[]
        
        for category in categoryListLocator:
            try:
                button=category.locator("button[class='btn-subcategory']")
            except:
                button=None

            categoryList.append({"name":category.locator("span").inner_text(),
                                "button":button})
        print(categoryList)
        #example

        #getting random number
        ##Use embeddings function to select the best category
        #categoryList=search_best_option(categoryList)
        categNumb=randrange(0,len(categoryList))
        print(categNumb)
        #selecting the category

        try:
            categoryList[categNumb]["button"].click()
        except:
            self.page.get_by_text(categoryList[categNumb]["name"]).click()
            print("Se llegó al último nivel de dicha categoría")
            return False
    
        print("Categoria seleccionada:"+categoryList[categNumb]["name"])
        return True
        #self.page.locator(".btn-subcategory").first.click()
        #self.page.locator(".btn-subcategory").first.click()
        #self.page.get_by_text("Aceite Vegetal").click()
        #print("categoria seleccionada")


    def load_all_category(self):

        self.page.get_by_label("Categoría", exact=True).get_by_role("textbox").click()
        while True:
            missingCategories=self.load_category()
            if not missingCategories:
                break
        print("Se cargaron todas las categorías")
        # #example
        # #categoryList[0]["button"].click()
        # self.page.locator(".btn-subcategory").first.click()
        # self.page.locator(".btn-subcategory").first.click()
        # self.page.get_by_text("Aceite Vegetal").click()
        # print("categoria seleccionada")
        
    def load_brand(self):
        self.page.locator("div[id='inputBrand']").click()
        brands_text=self.page.locator("div[id='inputBrand'] li[class='multiselect__element']").all_inner_texts()
        print(brands_text)
        try:
            brand_index = brands_text.index("GENÉRICO")
            print(brand_index)
        except:
            brand_index = -1
        self.page.locator(f"li:nth-child({brand_index+1}) > .multiselect__option").click()

    def load_site(self):
        time.sleep(1)
        sites_list=self.page.locator("div[id='__BVID__197_']>label>span>span").all()
        sites_list_text=self.page.locator("div[id='__BVID__197_']>label>span>span").all_inner_texts()
        print(sites_list_text)
        print("Seleccionando RealPlaza")
        sites_list[4].click()

    def load_aditional_fields(self):
        time.sleep(1)
        additional_fields_locator=self.page.locator("div[class='row mt-3 attr-row']").all()
        additional_fields_text=self.page.locator("div[class='row mt-3 attr-row'] legend").all_inner_texts()
        additional_fields=[]
        
        for additional_field in additional_fields_locator:

            if len(additional_field.locator("div[role='alert']").all())>0:
                mandatory=True
            else:
                mandatory=False

            type=additional_field.locator("input").all()[0].get_attribute("type")
            if type!="text":
                #options=additional_field.locator("input span").all_inner_texts()
                options=additional_field.locator("span span").all_inner_texts()
            else:
                options=[]
            name=additional_field.locator("legend").inner_text()
            additional_fields.append({"name":name,
                                      "mandatory":mandatory,
                                      "type":type,
                                      "options":options,
                                      "fieldObject":additional_field})
            
        mandatory_fields=[field for field in additional_fields if field["mandatory"]==True]
        
        print("Campos adicionales " + str(len(additional_fields)))
        print(additional_fields)
        print("-------------------")

        print("Campos obligatorios " + str(len(mandatory_fields)))
        print(mandatory_fields)
        print("-------------------")

        self.mandatory_fields=mandatory_fields

    def fill_mandatory_fields(self):

        for field in self.mandatory_fields:
            type=field["type"]

            if type=="text":
                field["fieldObject"].locator("input").fill("test")
            elif type=="check":
                field["fieldObject"].locator("input").first().check()
            elif type=="radio":
                field["fieldObject"].locator("input").first().check()
        print("Campos obligatorios llenados")

    def create_product(self):
        self.page.get_by_role("button", name="Guardar").click()
        self.page.get_by_role("button", name="OK").click()
        print("Producto creado")
        self.page.wait_for_load_state("networkidle")

    def create_variant(self):

        self.page.locator("[id=\"__BVID__228_\"]").fill("22") #UPC
        self.page.get_by_label("Crear variante para el").locator("#nombreFormatterHelp").fill("eee") #nombre
        #Precios
        self.page.get_by_role("textbox", name="Precio regular").fill("250")
        self.page.get_by_role("textbox", name="Precio con descuento").fill("200")
        self.page.get_by_role("textbox", name="Descuento válido desde").fill("2024-03-28")
        self.page.get_by_role("textbox", name="Descuento válido hasta").fill("2024-04-25")
        #Medidas
        self.page.get_by_role("textbox", name="Alto cm").fill("22")
        self.page.get_by_role("textbox", name="Ancho cm").fill("22")
        self.page.get_by_role("textbox", name="Largo cm").fill("22")
        self.page.get_by_role("textbox", name="Peso gr").fill("22")
        #Imagen
        #self.page.get_by_role("textbox", name="Seleccione un archivo").click()



        #print(additional_fields_locator)
        #print(additional_fields_text)
        #print("Se imprimieron los campos adicionales")
        #div[role='alert']
        #self.page.get_by_role("button", name="Guardar").click()
        #self.page.get_by_role("button", name="Cancelar").click()

#    def load_all_products(self):
#        loadDinners=LoaderDinners(self.dataToLoad)
#        for product in self.dataToLoad:
#            self.load_main_dinners(product)


        
class LoaderRP:
    def __init__(self,dataToLoad):
        self.dataToLoad=dataToLoad
        
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



if __name__ == "__main__":
    RPmloader=multiLoaderRP(2)
    RPmloader.go_to_create_product()
    print("---Paso 1: Crear Producto---")
    RPmloader.load_product_name()
    RPmloader.load_all_category()
    RPmloader.load_aditional_fields()
    RPmloader.fill_mandatory_fields()
    RPmloader.load_description()
    RPmloader.load_brand()
    RPmloader.load_site()
    RPmloader.create_product()   
    print("Producto Creado")
    print("---Paso 2: Crear Variantes---")
    RPmloader.create_variant()
    print("---Variante creada---")

    
#class="multiselect__element"

