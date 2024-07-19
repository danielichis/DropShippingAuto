import os
from playwright.sync_api import sync_playwright,expect
from utils.jsHandler import insertPropertiesToPage
from random import randrange
from datetime import date,timedelta
from utils.managePaths import mp
import json
import time
homeRealPlaza="https://inretail.mysellercenter.com/#/dashboard"
import re

class LoaderRealPlaza:
    def __init__(self,dataToLoad=None,page=None,context=None,p=None,sheetProductData=None,configSheetData=None):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
        self.sheetProductData=sheetProductData
        self.configDataSheet=configSheetData
    def start_playwright(self):
        self.p = sync_playwright().start()
        user_dir=mp.get_current_chrome_profile_path()
        #self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False,record_video_dir='videos/',slow_mo=50)
        self.browser= self.p.chromium.launch(headless=False)
        self.page=self.browser.new_page()
    def login_real_plaza(self):
        pass

    def handle_login_real_plaza(self):
        self.cookies=self.page.context.cookies()
        self.page.locator("form[name='userLogin'] button").click()
        if self.page.url.find("https://irmarketplace.us.auth0.com/login?state")!=-1:
            print("Se encuentra en la página de autenticación")
            self.page.locator("input[name='email']").fill("mkpinter@unaluka.com")
            self.page.locator("input[name='password']").fill("Inretail123*")
        self.page.wait_for_load_state("networkidle")
        print("Haciendo clik para loguearse")
        with self.page.expect_response("https://irmarketplace.us.auth0.com/oauth/token") as response_info:
            self.page.locator("g[id='Login']").click()
        response = response_info.value
        tokenLogin=response.json()["access_token"]
        self.token=tokenLogin

    def sear_category(self,category:str):
        urlEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/categories/?sortOrder=asc&sortBy=name.keyword&from=0&size=10&text=laptops"
        # cok=self.page.context.cookies()
        # contextApi=self.p.request.new_context(cookies=cok)
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        r=self.page.request.get(urlEndpoint,headers=header)
        print(r.json())
        #make get request to get categories with page.route
        print("Categoría buscada")
    def get_children_category_trought_api(self,categoryId:str):
        urlEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/categories/?sortOrder=asc&sortBy=name.keyword&from=0&size=100&parentId={categoryId}"
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        r=self.page.request.get(urlEndpoint,headers=header)
        return r.json()
    def get_childrens(self,child_of_child):
        if child_of_child['hasChildren']:
            child_of_child["children"]=self.get_children_category_trought_api(child_of_child['id'])
            for child in child_of_child["children"]:
                self.get_childrens(child)
            
    def get_tree_categories(self):
        rootUrl="https://inretail.mysellercenter.com/sellercenter/api/v1/categories/?sortOrder=asc&sortBy=name.keyword&from=0&size=100&root=true"
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        rootCategories=self.page.request.get(rootUrl,headers=header).json()
        for child in rootCategories:
            self.get_childrens(child)
        path_real_plaza_categories_json=mp.realPlazaTreeCategoriesJsonPath
        with open(path_real_plaza_categories_json, "w",encoding="utf-8") as f:
            json.dump(rootCategories, f, indent=4, ensure_ascii=False)
        print("Categorías guardadas en json")
        #query para obtener los nodos con el atributo hasChildren=False

    def go_to_home(self):
        self.page.goto(homeRealPlaza)
        self.page.wait_for_load_state("networkidle")
    def go_to_create_product(self):
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
        categNumb=randrange(0,len(categoryList))
        print(categNumb)

        try:
            categoryList[categNumb]["button"].click(timeout=2000)
        except:
            self.page.get_by_text(categoryList[categNumb]["name"],exact=True).click()
            print("Se llegó al último nivel de dicha categoría")
            print("Categoria seleccionada:"+categoryList[categNumb]["name"])
            return False
    
        print("Categoria seleccionada:"+categoryList[categNumb]["name"])
        return True

    def load_all_category(self):

        self.page.get_by_label("Categoría", exact=True).get_by_role("textbox").click()
        while True:
            missingCategories=self.load_category()
            if not missingCategories:
                break
        print("Se cargaron todas las categorías")
        self.page.wait_for_load_state("networkidle")

        
    def load_brand(self):
        self.page.locator("div[id='inputBrand']").click()
        brands_text=self.page.locator("div[id='inputBrand'] li[class='multiselect__element']").all_inner_texts()
        print(brands_text)
        try:
            brand_index = brands_text.index("YONKER")
            print(brand_index)
        except:
            brand_index = -1
        self.page.locator(f"li:nth-child({brand_index+1}) > .multiselect__option").click()

    def load_site(self):
        time.sleep(1)
        sites_list=self.page.locator("div[id='__BVID__206_']>label>span>span").all()
        #select all sites
        for site in sites_list:
            site.click()
        # sites_list_text=self.page.locator("div[id='__BVID__206_']>label>span>span").all_inner_texts()
        # print(sites_list_text)
        # print("Seleccionando RealPlaza")
        # sites_list[4].click()

    def get_additional_fields(self):
        time.sleep(2)
        expect(self.page.locator("div[class='row mt-3 attr-row']").first).not_to_be_empty()
        additional_fields_locator=self.page.locator("div[class='row mt-3 attr-row']").all()
        additional_fields_text=self.page.locator("div[class='row mt-3 attr-row'] legend").all_inner_texts()
        additional_fields=[]
        
        for additional_field in additional_fields_locator:

            if len(additional_field.locator("div[role='alert']").all())>0:
                mandatory=True
            else:
                mandatory=False

            type=additional_field.locator("input").first.get_attribute("type")
            if type!="text" or type!="number":
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
        #storing mandatory and additional fields on the object
        self.mandatory_fields=mandatory_fields
        self.additional_fields=additional_fields
    
    def load_additional_fields(self):
        pass
    def fill_mandatory_fields(self):
        
        for field in self.mandatory_fields:
            type=field["type"]
            
            if type=="text":
                field["fieldObject"].locator("input").fill("test")
            elif type=="number":
                field["fieldObject"].locator("input").fill("2")
            elif type=="checkbox":
                #field["fieldObject"].locator("input").first().check()
                for check_label in field["options"]:
                    print(check_label)
                    #field["fieldObject"].locator("input").all()[0].check()
                    #field["fieldObject"].get_by_label(check_label,exact=True).check()
                    field["fieldObject"].get_by_text(check_label,exact=True).first.click()
            elif type=="radio":
                #field["fieldObject"].locator("input").first().check()
                radio_label=label=field["options"][0]
                print(radio_label)
                #field["fieldObject"].locator("input").all()[0].check()
                #field["fieldObject"].get_by_text(radio_label,exact=True).click()
                field["fieldObject"].get_by_text(radio_label,exact=True).first.click()
            else:
                print(type)
                field["fieldObject"].locator("input").fill("test")
                
        print("Campos obligatorios llenados")

    def create_product(self):
        self.page.get_by_role("button", name="Guardar").click()
        self.page.get_by_role("button", name="OK").click()
        print("Producto guardado")
        self.page.wait_for_load_state("networkidle")

    def create_variant(self):

        self.page.locator("#__BVID__237_").fill("22") #UPC
        self.page.get_by_label("Crear variante para el").locator("#nombreFormatterHelp").fill("eee") #nombre
        #Precios
        self.page.get_by_role("textbox", name="Precio regular").fill("250")
        self.page.get_by_role("textbox", name="Precio con descuento").fill("200")

        #Obteniendo fechas
        from_date = date.today()
        until_date=from_date+timedelta(days=5)
        from_str=from_date.strftime("%Y-%m-%d")
        until_str=until_date.strftime("%Y-%m-%d")
        from_day_str=from_date.strftime("%#d")
        until_day_str=until_date.strftime("%#d")
        print("Fechas de descuento:", from_str,until_str)
        print("dias:",from_day_str,until_day_str)
        #LLenando fechas
        #solve later
        #self.page.get_by_role("textbox", name="Descuento valido desde").fill(from_str)
        #self.page.get_by_role("textbox", name="Descuento válido hasta").fill(until_str)
        #Llenando fechas 2
        self.page.get_by_label("Descuento válido desde").get_by_role("textbox").click()
        self.page.locator(f"td[title='{from_str}']").first.click()
        self.page.get_by_label("Descuento válido hasta").get_by_role("textbox").click()
        self.page.locator(f"td[title='{until_str}']").first.click()
        #Medidas
        self.page.get_by_role("textbox", name="Alto cm").fill("22")
        self.page.get_by_role("textbox", name="Ancho cm").fill("22")
        self.page.get_by_role("textbox", name="Largo cm").fill("22")
        self.page.get_by_role("textbox", name="Peso gr").fill("22")
        #Imagen
        #self.page.get_by_role("textbox", name="Seleccione un archivo").click()
        self.load_img()
        #Select button 
        self.page.get_by_label("Crear variante para el").get_by_role("button", name="Crear Variante").click()
        self.page.wait_for_load_state("networkidle")
        #save variant
        self.page.get_by_role("button", name="Guardar").click()
        self.page.get_by_role("button", name="OK").click()
        self.page.wait_for_load_state("networkidle")
        #storing SKU and ID of product
        self.variant_sku=self.page.locator("td[data-label='SKU']>div").inner_text()
        self.page.get_by_text("Datos del Producto").click()
        self.product_id=self.page.locator("input[id='idInput']").input_value()
        print("SKU del producto creado: "+self.variant_sku)
        print("ID del producto creado: "+ self.product_id)
        
    def load_img(self):
        #self.page.get_by_role("textbox", name="Seleccione un archivo").click()
        test_sku_path=os.path.join(mp.sku_folder_path,"B0BGHRMJ1B","images","originals")
        imagesList=os.listdir(test_sku_path)
        fullPaths=[]
        for image in imagesList:
            fullPath=os.path.join(test_sku_path,image)
            fullPaths.append(fullPath)
        self.page.locator("input[type='file']").first.set_input_files(fullPaths[0])

    def update_inventory_number(self):
        self.page.get_by_role("navigation").get_by_text("Inventario", exact=True).click()
        self.page.get_by_role("link", name="Administrar Inventario").click()
        self.page.wait_for_load_state("networkidle")
        print("Buscando producto por ID")
        self.page.locator("tr[role='row']").filter(has_text=self.product_id).locator("td[aria-colindex='5'] button").click()
        #self.page.locator("tr[role='row']").all()[0].locator("td[aria-colindex='8'] button").click()
        print("Se abrió la ventana de editar inventario")
        print("buscando variante por SKU")
        self.page.locator("tr[role='row']").filter(has_text=self.variant_sku).locator("td[aria-colindex='5'] span[class='inventoryTotal']").click()
        self.page.get_by_role("textbox", name="Nuevo valor de inventario").fill("1")
        self.page.get_by_role("button", name="Guardar").click()
        self.page.wait_for_load_state("networkidle")
        print("Inventario de variante actualizado a 1")
    def end_playwright(self):
        self.browser.close()
        self.p.stop()
        print("Playwright cerrado")
    def load_main_real_plaza(self):
        self.go_to_home()
        self.handle_login_real_plaza()
        self.go_to_create_product()
        print("---Paso 1: Crear Producto---")
        #self.get_tree_categories()
        #self.sear_category("laptops")
        self.load_product_name()
        self.load_all_category()
        self.get_additional_fields()
        self.load_additional_fields()
        self.fill_mandatory_fields()
        self.load_description()
        self.load_brand()
        self.load_site()
        self.create_product()   
        print("Producto Creado")
        print("---Paso 2: Crear Variantes---")
        self.create_variant()
        print("---Variante creada---")
        self.update_inventory_number()
        print("Producto creado y variante creada")
        print("Regresando a la página de crear producto")
        self.go_to_home()
        self.go_to_create_product()
        self.end_playwright()   
def test_get_tree_categories():
    pass
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


def other_tests():
    test_sku_path=os.path.join(mp.sku_folder_path,"B0BGHRMJ1B","images","originals")
    imagesList=os.listdir(test_sku_path)
    print(imagesList)

if __name__ == "__main__":
    #other_tests()
    RPmloader=LoaderRealPlaza()
    RPmloader.start_playwright()
    RPmloader.load_main_real_plaza()
    
