from playwright.sync_api import sync_playwright,expect
from utils.jsHandler import insertPropertiesToPage
#from DropShippingAuto.src.utils.dinamySelections import search_best_option
#from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
#from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction
from utils.managePaths import mp
import json
import time
homeRipley="https://ripleyperu-prod.mirakl.net/login"
import re
from random import randrange
from datetime import date,timedelta
#from img_sizer1000x1000 import resize_image


class multiLoaderRIP:
    def __init__(self,dataToLoad):
        self.dataToLoad=dataToLoad
        self.p = sync_playwright().start()
        user_dir=r"C:\Users\risin\AppData\Local\Google\Chrome\UserData2"
        self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False,record_video_dir='videos/')
        self.page=self.browser.new_page()
    
    def go_to_create_product(self):
        self.page.goto(homeRipley)
        self.page.get_by_text("Añadir una oferta").click()
        self.page.get_by_role("link", name="+ Crear un producto").click()
        print("pagina cargada")

    def make_category_list(self)->list:
        categories_list_locator=self.page.locator("div[class='select2-result-label']").all()
        categories_list=[]
        for category in categories_list_locator:
            categories_list.append({"name":category.inner_text(),"locator":category})

        print(categories_list)
        return categories_list

    def load_all_category(self):

        cat_num=0
        while(True):
            next_locator=self.page.locator("div[id='next"+str(cat_num)+"']")
            try:
                next_locator.locator("div[class='input col-md-4 col-lg-4']").click(timeout=3000)
                categories_list=self.make_category_list()
                
                #Select a random category
                categNumb=randrange(0,len(categories_list))
                print(categNumb)
                categories_list[categNumb]["locator"].click()
                print("Categoria seleccionada")
                cat_num+=1
            except:
                print("No hay más categorías por seleccionar")
                break

        print("Se cargaron todas las categorías")

    def load_section2_product_char(self):

        divs2_names=self.page.locator("div[id='productCreationForm'] div[id*='productCreationFormField'][style='display:block'] label[class='required']").all_inner_texts()
        divs2_locators=[]
        
        for name in divs2_names:
            divs2_locators.append({"name":name,
                                   "locator":self.page.get_by_label(name,exact=True).first,
                                   #"tag_name":self.page.get_by_label(name,exact=True).first.evaluate("element => element.tagName")
                                   })

        print("Campos de la sección 2")
        print(divs2_names)
        print(divs2_locators)

        for loc in divs2_locators:

            try:
                loc["locator"].fill("test",timeout=3000)
            except Exception as e:
                print(e)
                print("Not a fillable element")
                continue


        print("Se imprimieron los nombres de la seccion Caracteristicas del Producto")
        
    def load_section_offer_char(self):

        divs4_names=self.page.locator("div[id='ui-id-0'] div[id^='variantFormField-ui-id-0'][style='display:block'] label[class='required']").all_inner_texts()
        divs4_locators=[]
        
        for name in divs4_names:
            divs4_locators.append({"name":name,
                                   "locator":self.page.get_by_label(name,exact=True).first,
                                   #"tag_name":self.page.get_by_label(name,exact=True).first.evaluate("element => element.tagName")
                                   })

        print("Campos de la sección 4 :Caracteristicas de la Oferta")
        print(divs4_names)
        print(divs4_locators)

        for loc in divs4_locators:

            try:
                loc["locator"].fill("test",timeout=3000)
            except Exception as e:
                print(e)
                print("Not a fillable element")
                continue


        print("Se imprimieron los nombres de la seccion 2")

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
            categoryList[categNumb]["button"].click(timeout=2000)
        except:
            self.page.get_by_text(categoryList[categNumb]["name"],exact=True).click()
            print("Se llegó al último nivel de dicha categoría")
            print("Categoria seleccionada:"+categoryList[categNumb]["name"])
            return False
    
        print("Categoria seleccionada:"+categoryList[categNumb]["name"])
        return True
        #self.page.locator(".btn-subcategory").first.click()
        #self.page.locator(".btn-subcategory").first.click()
        #self.page.get_by_text("Aceite Vegetal").click()
        #print("categoria seleccionada")

    
    



    # def load_all_category(self):

    #     self.page.get_by_label("Categoría", exact=True).get_by_role("textbox").click()
    #     while True:
    #         missingCategories=self.load_category()
    #         if not missingCategories:
    #             break
    #     print("Se cargaron todas las categorías")
    #     self.page.wait_for_load_state("networkidle")

        
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
        print("Producto creado")
        self.page.wait_for_load_state("networkidle")

    def create_variant(self):

        self.page.locator("[id=\"__BVID__228_\"]").fill("22") #UPC
        self.page.get_by_label("Crear variante para el").locator("#nombreFormatterHelp").fill("eee") #nombre
        #Precios
        self.page.get_by_role("textbox", name="Precio regular").fill("250")
        self.page.get_by_role("textbox", name="Precio con descuento").fill("200")

        #Obteniendo fechas
        from_date = date.today()
        until_date=from_date+timedelta(days=5)
        from_str=from_date.strftime("%Y-%m-%d")
        until_str=until_date.strftime("%Y-%m-%d")
        print("Fechas de descuento:", from_str,until_str)

        #LLenando fechas
        self.page.get_by_role("textbox", name="Descuento válido desde").fill(from_str)
        self.page.get_by_role("textbox", name="Descuento válido hasta").fill(until_str)
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
        print(self.variant_sku)
        print(self.product_id)
        
    def load_img(self):
        #self.page.get_by_role("textbox", name="Seleccione un archivo").click()
        img_route=r"C:\Users\risin\Downloads\imgTest\test2.jpg"
        img_route_resized=r"C:\Users\risin\Downloads\imgTest\test_1_resized.jpg"
        print("Convirtiendo imagen a 1000x1000...")
        resize_image(img_route,img_route_resized)
        print("Imagen convertida")
        self.page.locator("input[type='file']").first.set_input_files(img_route_resized)

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

    

if __name__ == "__main__":
    RIPmloader=multiLoaderRIP(2)
    RIPmloader.go_to_create_product()
    RIPmloader.load_all_category()
    RIPmloader.load_section2_product_char()
    RIPmloader.load_section_offer_char()
    # RPmloader.go_to_create_product()
    # print("---Paso 1: Crear Producto---")
    # RPmloader.load_product_name()
    # RPmloader.load_all_category()
    # RPmloader.load_aditional_fields()
    # RPmloader.fill_mandatory_fields()
    # RPmloader.load_description()
    # RPmloader.load_brand()
    # RPmloader.load_site()
    # RPmloader.create_product()   
    # print("Producto Creado")
    # print("---Paso 2: Crear Variantes---")
    # RPmloader.create_variant()
    # print("---Variante creada---")
    # RPmloader.update_inventory_number()
    # print("Producto creado y variante creada")
    # print("Regresando a la página de crear producto")
    # RPmloader.go_to_create_product()
    

    
#class="multiselect__element"

