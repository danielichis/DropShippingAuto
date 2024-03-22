from playwright.sync_api import sync_playwright
from DropShippingAuto.src.utilsDropSh.dinamySelections import search_best_option
from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction
from utils.embeddings.embeding import get_best_similarity_option
from utils.managePaths import mp
from utils.jsHandler import insertPropertiesToPage
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
        self.page.goto(homeDinners)
        if self.page.get_by_text("Hello! Log in with your email.").is_visible():
            print("pide login")
            self.login_dinners()
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
            self.go_to_create_product()

        
class LoaderDinners():
    def __init__(self,dataToLoad,page,context,p):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
    def on_success(self,response):
        print("Success")
        print(response.ok, response.request.method)
    def on_error(self,response):
        print(response.ok, response.status_text)
        print("Error")
    def create_new_product(self):
        with self.page.expect_response("https://api.quickcomm.co/catalog/products",timeout=4000) as response_info:
            self.page.locator("product-create button[type=submit]").click()
        response = response_info.value
        return response.ok
    def load_seller(self):
        self.page.locator("//span[text()='Vendedor']//parent::div//input").click()
        self.page.locator("//a[text()='UNALUKA INTERNACIONAL']").click()

    def load_brand(self):
        marca_a_buscar=self.dataToLoad['data']['marca']
        self.page.locator("//span[text()='Marca']//parent::div//input").type(marca_a_buscar,delay=100)
        time.sleep(0.5)
        try:
            self.page.wait_for_selector("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']",timeout=5000)
            lista_marcas=self.page.locator("//span[text()='Marca']/parent::div//a[@class='ng-star-inserted']").all_inner_texts()
            best_option=search_best_option(marca_a_buscar,lista_marcas,"-")
            self.page.locator("a").filter(has_text=re.compile(rf"^{best_option}$")).click()
        except:
            print("no se encontro marca, marca nueba")

    def load_category(self):
        categoria=self.dataToLoad['data']['categoria']
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
        upc=get_upc(self.dataToLoad['data']['sku'])
        self.page.locator("div").filter(has_text=re.compile(r"^Código InternoIdentificador unico \(Opcional\)$")).get_by_role("textbox").fill(upc)
        self.page.query_selector("input[formcontrolname='barCode']").fill(upc)

    def load_name_product(self):
        name_product=self.dataToLoad['data']['nombreProducto']
        self.page.locator("div").filter(has_text=re.compile(r"^Nombre Producto$")).get_by_role("textbox").fill(name_product)

    def load_description(self):
        description=self.dataToLoad['data']['descripcion']
        self.page.locator("//div[@class='ngx-editor-textarea']").fill("---")
        insertPropertiesToPage("div[class='ngx-editor-textarea']",description,self.page)
        

    def load_base_price(self):
        base_price=self.dataToLoad['data']['precioAmazon'] 
        base_price=str(round(float(re.findall(r"(\d+\.\d+)",base_price)[0]),2))
        self.page.locator("div").filter(has_text=re.compile(r"^Precio Base$")).get_by_role("spinbutton").fill(base_price)

    def load_special_price(self):
        special_price=self.dataToLoad['data']['precioAmazon']
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
        sku=self.dataToLoad['data']['sku']
        self.page.locator("div").filter(has_text=re.compile(r"^SKU \(código de artículo\)$")).get_by_role("textbox").fill(sku)
    def load_stock(self):
        stock="1"
        self.page.locator("div").filter(has_text=re.compile(r"^Stock$")).get_by_role("spinbutton").fill(stock)

    def load_dimensions(self):
        dimensions=self.dataToLoad['data']['dimensions_cm']
        self.page.get_by_placeholder("Largo cm").fill(str(25))
        self.page.get_by_placeholder("Ancho cm").fill(str(25))
        self.page.get_by_placeholder("Altura cm").fill(str(25))
        self.page.get_by_placeholder("Peso").fill(str(200))

    def load_images(self):
        for imagePath in self.dataToLoad["data"]["imagesPath"]:
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
        contentProduct=mp.data_sku(self.dataToLoad['data']['sku'])
        dimArgs=get_dinamic_args_extraction(content_product=str(contentProduct),fieldsFromMarketPlace=mandatorySelectFields)
        dimArgs=json.loads(dimArgs)
        for field in mandatorySelectFields:
            textField=field["name"]
            valueField=dimArgs[textField]
            if field["fieldType"]=="input":
                field["fieldObject"].query_selector("input").fill(valueField)
            elif field["fieldType"]=="select":
                if valueField in field["options"]:
                    optionToSelect=valueField
                else:
                    optionToSelect=get_best_similarity_option(field["options"],valueField)
                field["fieldObject"].query_selector("select").select_option(optionToSelect)
                print("selecion hecha")    
        
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
        self.create_new_product()
if __name__ == "__main__":
    mloader=multiLoaderDinners(infoDinnersToLoad)
    mloader.go_to_create_product()
    mloader.load_all_products()

    
