from playwright.sync_api import sync_playwright,expect
from DropShippingAuto.src.utilsDropSh.dinamySelections import search_best_option
from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction
from utils.embeddings.embeding import get_best_similarity_option,get_best_category_dinners
from utils.managePaths import mp
from DropShippingAuto.src.marketPlacesDestino.dinners.embeddingsFiedls import get_brand_dinners,get_brand_with_f_calling
from utils.jsHandler import insertPropertiesToPage
import traceback
import json
import time
homeDinners="https://admin.quickcomm.co/catalog/products"
import re


class multiLoaderDinners:
    def __init__(self,dataToLoad):
        self.dataToLoad=dataToLoad
        self.p = sync_playwright().start()
        user_dir=mp.get_current_chrome_profile_path()
        self.context = self.p.chromium.launch_persistent_context(user_dir,headless=False)
        self.page=self.context.new_page()
    
    def go_to_create_product(self):
        self.page.get_by_role("button", name=" Crear Producto").click()
        self.page.get_by_role("button", name=" Empezar").click()

    def login_dinners(self):
        self.page.locator("button[class='btn btn-main']").click()
        self.page.locator("i[class='fas fa-sign-in-alt']").click()
        pass

    def load_all_products(self):
        print(self.dataToLoad)
        for productData in self.dataToLoad:
            loadDinners=LoaderDinners(productData,self.page,self.context,self.p)
            loadDinners.load_main_dinners()
            r=loadDinners.create_new_product()
            if r:
                print("Producto creado")
            else:
                print("Error al crear producto,cerraando ventana del producto")
            loadDinners.go_to_create_product()

        
class LoaderDinners():
    def __init__(self,dataToLoad,sheetProductData,configSheetData,page,context,p):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
        self.sheetProductData=sheetProductData
        self.configSheetData=configSheetData
    def login_dinners(self):
        self.page.locator("button[class='btn btn-main']").click()
        self.page.locator("i[class='fas fa-sign-in-alt']").click()
        pass
    def handle_login_dinners(self):
        try:
            expect(self.page).to_have_url(re.compile(mp.newProductDinners))
        except:
            if self.page.url=="https://admin.quickcomm.co/auth/login":
                self.page.fill("input[id='input-email']","mkpinter@unaluka.com")
                self.page.fill("input[id='input-password']","Unaluk@Flash23")
                #click login text with hast text
                self.page.click("button:has-text('Log In')")
                self.page.wait_for_url("https://admin.quickcomm.co/")
                self.page.goto(mp.newProductDinners)
                #wait for url to change
                expect(self.page).to_have_url(re.compile(mp.newProductDinners))
                print("updating login")
    def go_to_create_product(self):
        self.page.get_by_role("button", name=" Crear Producto").click()
        self.page.get_by_role("button", name=" Empezar").click()
    def on_success(self,response):
        print("Success")
        print(response.ok, response.request.method)
    def on_error(self,response):
        print(response.ok, response.status_text)
        print("Error")
    def create_new_product(self):
        with self.page.expect_response("https://api.quickcomm.co/catalog/products",timeout=8000) as response_info:
            self.page.locator("product-create button[type=submit]").click()
        response = response_info.value
        if response.ok:
            self.statusLoad="Cargado Correctamente"
            self.condition="NEW"
        elif response.status==409:
            self.statusLoad="NO SE CARGÓ,El PRODUCTO YA EXISTE"
            self.condition="NO"
        else:
            self.statusLoad="ERROR EN LA CARGA"
    def load_seller(self):
        self.page.locator("//span[text()='Vendedor']//parent::div//input").click()
        self.page.locator("//a[text()='UNALUKA INTERNACIONAL']").click()

    def load_brand(self):
        self.page.locator("//span[text()='Marca']//parent::div//input").click()
        lista_marcas=self.page.locator("li div a[class='ng-star-inserted']").all_inner_texts()
        if len(lista_marcas)==0:
            time.sleep(2)
            lista_marcas=self.page.locator("li div a[class='ng-star-inserted']").all_inner_texts()
        marca_a_buscar=get_brand_with_f_calling(self.dataToLoad)
        self.page.locator("//span[text()='Marca']//parent::div//input").type(marca_a_buscar,delay=100)
        time.sleep(0.5)
        #self.page.wait_for_selector("li div a[class='ng-star-inserted']")
        lista_marcas=self.page.locator("li div a[class='ng-star-inserted']").all_inner_texts()
        if marca_a_buscar in lista_marcas:
            self.page.locator("a").filter(has_text=re.compile(rf"^{marca_a_buscar}$")).click()
        else:
            pass
            #self.page.locator("a").filter(has_text="PSB").click()

    def load_category(self):
        amazonCategories=self.dataToLoad['clasificacion']
        amazonCategories.reverse()
        categoryToWrite=get_best_category_dinners(str(amazonCategories))
        self.page.locator("//span[text()='Categoría']//parent::div//input").click()
        self.page.locator("a").filter(has_text=re.compile(rf"^{categoryToWrite}$")).click()
        print("Categoria seleccionada")
        # for cate in amazonCategories:
        #     self.page.locator("//span[text()='Categoría']//parent::div//input").type(cate,delay=100)
        #     lista_categorias=self.page.locator("//span[text()='Categoría']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
        #     if len(lista_categorias)>0:
        #         best_option=search_best_option(cate,lista_categorias,"-")
        #         self.page.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()
        #         break
        #     else:
        #         self.page.locator("//span[text()='Categoría']//parent::div//input").fill("")
    def load_stock(self):
        stock="1"
        self.page.locator("//span[text()='Stock']//parent::div/input").fill(stock)
    def load_upc(self):
        upc=get_upc(self.dataToLoad['sku'])
        self.page.locator("div").filter(has_text=re.compile(r"^Código InternoIdentificador unico \(Opcional\)$")).get_by_role("textbox").fill(upc)
        self.page.query_selector("input[formcontrolname='barCode']").fill(upc)

    def load_name_product(self):
        name_product=self.dataToLoad['titulo']
        self.page.locator("div").filter(has_text=re.compile(r"^Nombre Producto$")).get_by_role("textbox").fill(name_product)

    def load_description(self):
        description=self.dataToLoad['descripciones']
        self.page.locator("//div[@class='ngx-editor-textarea']").fill("---")
        insertPropertiesToPage("div[class='ngx-editor-textarea']",description,self.page)
        self.page.locator("//div[@class='ngx-editor-textarea']").press("Enter")
        #self.page.locator("//div[@class='ngx-editor-textarea']").type("---")
        print("Descripción cargada")
        

    def load_base_price(self):
        base_price=str(self.sheetProductData['PRECIO LISTA MARKETPLACE'])
        #base_price=str(round(float(re.findall(r"(\d+\.\d+)",base_price)[0]),2))
        self.page.locator("div").filter(has_text=re.compile(r"^Precio Base$")).get_by_role("spinbutton").fill(base_price)

    def load_special_price(self):
        special_price=str(self.sheetProductData['PRECIO FINAL MARKETPLACE'])
        #special_price=str(round(float(re.findall(r"(\d+\.\d+)",special_price)[0]),2))
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
        sku=self.dataToLoad['sku']
        self.page.locator("div").filter(has_text=re.compile(r"^SKU \(código de artículo\)$")).get_by_role("textbox").fill(sku)
    def load_stock(self):
        stock="1"
        self.page.locator("div").filter(has_text=re.compile(r"^Stock$")).get_by_role("spinbutton").fill(stock)

    def load_dimensions(self):
        dimensions=self.dataToLoad['dimensions_cm']
        self.page.get_by_placeholder("Largo cm").fill(str(dimensions["Largo cm"]))
        self.page.get_by_placeholder("Ancho cm").fill(str(dimensions["Ancho cm"]))
        self.page.get_by_placeholder("Altura cm").fill(str(dimensions["Altura cm"]))
        self.page.get_by_placeholder("Peso").fill(str(dimensions["peso_kg"]))

    def load_images(self):
        for imagePath in self.dataToLoad["imagesPath"]:
            self.page.locator(".uploaded-photos__item > input").first.set_input_files(imagePath)

    def load_aditional_fields(self):
        self.page.wait_for_selector("div[class='col-md-6 ng-star-inserted']")
        aditionalFields=self.page.query_selector_all("div[class='col-md-6 ng-star-inserted']")
        fieldsData=[]
        for i,field in enumerate(aditionalFields):
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
                "fieldType":type,
                "fieldObject":field
            }

            fieldsData.append(fieldData)
        mandatorySelectFields=[field for field in fieldsData if field["mandatory"]==True]
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        dimArgs=get_dinamic_args_extraction(content_product=str(contentProduct),fieldsFromMarketPlace=mandatorySelectFields)
        for field in mandatorySelectFields:
            textField=field["name"]
            if field["fieldType"]=="input":
                valueField=dimArgs[textField]
                field["fieldObject"].query_selector("input").fill(valueField)
            elif field["fieldType"]=="select":
                try:
                    valueField=dimArgs[textField]
                except:
                    valueField="No Especifica"
                if valueField in field["options"]:
                    optionToSelect=valueField
                else:
                    optionToSelect=get_best_similarity_option(field["options"],valueField)
                field["fieldObject"].query_selector("select").select_option(optionToSelect)
                print("selecion hecha")    
        
    def load_main_dinners(self):
        self.go_to_create_product()
        try:
            self.load_images()
            self.load_seller()
            self.load_category()
            self.load_brand()
            self.load_name_product()
            self.load_description()
            self.load_stock()
            self.load_base_price()
            self.load_special_price()
            self.load_sku()
            self.load_upc()
            self.load_dimensions()
            self.load_aditional_fields()
            self.create_new_product()
            url=self.page.url
            tb="ok"
        except Exception as e:
            tb=traceback.format_exc()
            url="-"
            self.statusLoad="ERROR EN LA CARGA"
            self.condition="-"
        responseLoad={
            "sku":self.dataToLoad['sku'],
            "status":self.statusLoad,
            "url":url,
            "marketplace":"dinners",
            "condition":self.condition,
            "log":tb,
            "fecha":time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.responseDinnersLoad=responseLoad
        
if __name__ == "__main__":
    pass
    # mloader=multiLoaderDinners(infoDinnersToLoad)
    # mloader.go_to_create_product()
    # mloader.load_all_products()

    
