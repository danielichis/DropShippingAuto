from playwright.sync_api import sync_playwright
#from DropShippingAuto.src.utils.dinamySelections import search_best_option
#from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
#from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
import json
import time
homeRealPlaza="https://inretail.mysellercenter.com/#/dashboard"
import re


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

    def load_aditional_fields(self):
        self.page.get_by_label("Categoría", exact=True).get_by_role("textbox").click()
        self.page.locator(".btn-subcategory").first.click()
        self.page.locator(".btn-subcategory").first.click()
        self.page.get_by_text("Aceite Vegetal").click()
        print("categoria seleccionada")
        aditional_fields=self.page.locator("div[class='row mt-3 attr-row'] legend").all_inner_texts()
        print(aditional_fields)
        print("Se imprimieron los campos adicionales")


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
    RPmloader.load_aditional_fields()
    print("terminado")

    
