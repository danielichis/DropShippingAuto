from playwright.sync_api import sync_playwright,expect
from utils.jsHandler import insertPropertiesToPage
#from DropShippingAuto.src.utils.dinamySelections import search_best_option
#from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
#from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
#from utils.dinamicMassivArgsExtractions import get_dinamic_args_extraction
from utils.managePaths import mp
from StringHandling import extract_number_of_for,get_id_ul,get_first_enabled_locator
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
        user_dir=mp.get_current_chrome_profile_path()
        self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False)
        self.page=self.browser.new_page()

    def to_login(self):
        print("Iniciando sesion...")
        user_name="mkpinter@unaluka.com"
        user_password="Unaluk@Flash*"
        self.page.get_by_placeholder("Tu inicio de sesión").fill(user_name)
        self.page.get_by_role("button",name="Siguiente").click()
        self.page.get_by_label("Password*").fill(user_password)
        self.page.get_by_role("button",name="Sign in").click()
        print("Sesion iniciada")
    
    def go_to_home(self):
        self.page.goto(homeRipley)
        self.to_login()
        self.page.get_by_text("Añadir una oferta").click()

    def add_product(self):
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
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state('domcontentloaded')
        self.page.wait_for_load_state('load')

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
    
    def add_tag_n_attributes(self,locators_list:list)->list:

        for loc in locators_list:
            try:
                tag=loc["locator"].evaluate("element => element.nodeName",timeout=3000)
                attributes=loc["locator"].evaluate("element => element.getAttributeNames()")
            except:
                tag="Not found"
                attributes=[]
            
            key_values={}
            
            for attribute in attributes:
                key_values[attribute]=loc["locator"].evaluate(f"element => element.getAttribute('{attribute}')")    
            
            loc["tag"]=tag
            loc["key_values"]=key_values

            print(loc["name"]+"-"+loc["tag"])
            print(loc["key_values"])

        print("Se obtuvieron el tag y los atributos de los locators")

        
    def get_options_locator_list(self,locators_list:list)->list:

        for locator in locators_list:
            if locator["tag"]=="SELECT":
                options_list_locator=locator["locator"].locator("option").all_inner_texts()
                # options_list=[]
                # for option in options_list_locator:
                #     options_list.append({"name":option.inner_text(),
                #                         "locator":option})
                # locator["options"]=options_list
                locator["options"]=options_list_locator
                print(options_list_locator)
            elif locator["tag"]=="TEXTAREA":
                locator["options"]=[]
            elif locator["tag"]=="INPUT":
                if "aria-owns" in locator["key_values"]:
                    #makeclick using role
                    #self.page.get_by_role("combobox", name=locator["name"]).click()
                    try:
                        title=locator.get("name")
                        combobox_locator=self.page.locator("div[class='input col-md-4 col-lg-4']").filter(has=self.page.locator(f"input:enabled[title='{title}']")).first.click()
                    except Exception as e:
                        print("Error al hacer click en combobox"+str(e))
                        print("Pasando a siguiente elemento")
                        continue
                    id=locator["key_values"]["aria-owns"]
                    options_list_locator=self.page.locator(f"#{id}").locator("li").all()
                    options=[]
                    for item in options_list_locator:
                        options.append({"name":item.inner_text(),
                                        "locator":item})
                    print(id)
                    print([x["name"] for x in options])
                    locator["combobox"]=combobox_locator
                    locator["options"]=options
                    #select first option 
                    locator["options"][0]["locator"].click()
                elif "value" in locator["key_values"]:
                    print("Se encontró input")
                    locator["options"]=[]
                    print("INPUT + value")
            else:
                print("puede ser imagen")
                print(locator["tag"])
                locator["options"]=["IMG"]

        print("Se obtuvieron opciones de los locators")


    def get_options_locator_list2(self,locators_list:list)->list:

        for locator in locators_list:
            if locator["tag"]=="SELECT":
                options_list_locator=locator["locator"].locator("option").all()
                options_list=[]
                for option in options_list_locator:
                    options_list.append({"name":option.inner_text(),
                                         "locator":option})
                locator["options"]=options_list
                print([x["name"] for x in options_list])

            elif locator["tag"]=="TEXTAREA":
                locator["options"]=[]
            elif locator["tag"]=="INPUT":
                if "aria-owns" in locator["key_values"]:
                    #makeclick using role
                    #self.page.get_by_role("combobox", name=locator["name"]).click()
                    title=locator.get("name")
                    hidden_label=self.page.locator("label:visible[for^='s2id']").filter(has_text=title)
                    for_attribute=hidden_label.get_attribute("for")
                    id_ul=get_id_ul(for_attribute)
                    print(id_ul)
                    try:
                        combobox_locator=self.page.locator("div[class='input col-md-4 col-lg-4']").filter(has=self.page.locator(f"input:enabled[title='{title}']")).first
                        combobox_locator.click()
                        #getting id of unordered list of options with through the hidden label which contains the number in the id of the unordered list
                        #how to compute the string
                        #id for unordered list of results>s2-results-{number}
                        #will obtain the number from the id of the label ,the id in the label has the form s2id_autogen{number}

                    except Exception as e:
                        print("Error al hacer click en combobox"+str(e))
                        print("Pasando a siguiente elemento")
                        continue
                    #id=locator["key_values"]["aria-owns"]
                    options_list_locator=self.page.locator(f"#{id_ul}").locator("li").all()
                    options=[]
                    for item in options_list_locator:
                        options.append({"name":item.inner_text(),
                                        "locator":item})
                    print(id)
                    print([x["name"] for x in options])
                    #locator["combobox"]=combobox_locator
                    locator["options"]=options
                    #select first option 
                    locator["options"][0]["locator"].click()
                    #update locator with combobox locator
                    locator["locator"]=combobox_locator
                elif "value" in locator["key_values"]:
                    print("Se encontró input")
                    locator["options"]=[]
                    print("INPUT + value")
            else:
                print("puede ser imagen")
                print(locator["tag"])
                locator["options"]=["IMG"]

        print("Se obtuvieron opciones de los locators")

    def test_locators_list(self,locators_list:list)->None:

        for loc in locators_list:
            print(loc["name"]+"-"+loc["tag"])
            if len(loc["options"])==0:
                try:
                    if loc['name']=='Cantidad de la oferta' or loc['name']=='Precio':
                        loc["locator"].fill("25")
                    else:
                        loc["locator"].fill("TEST MODAFUCKAAAA")
                except Exception as e:
                    print("error"+str(e))
                    print("Pasando a siguiente elemento")
                    continue
            else:
                categNumb=randrange(0,len(loc["options"]))
                print(categNumb)
                if loc["tag"]=="SELECT":
                    option_label=loc["options"][categNumb]["name"]
                    loc["locator"].select_option(label=option_label)
                elif loc["tag"]=="INPUT":
                    loc["locator"].click()
                    loc["options"][categNumb]["locator"].click()
                print("Element selected")

        print("Se seleccionaron elementos")   
        # for loc in locators_list:
        #     try:
        #         loc["locator"].fill("test",timeout=3000)
        #         #loc["locator"].click(timeout=3000)
        #     except Exception as e:
        #         print(e)
        #         print("Not a fillable element")
        #         continue   


        
    def load_section_offer_char(self):

        #self.page.get_by_label("Marca",exact=True).first.click()
        #print("Se hizo click en la marca")

        #divs4_names=self.page.locator("div[id='ui-id-0'] div[id^='variantFormField-ui-id-0'][style='display:block'] label[class='required']").all_inner_texts()
        #divs4_names=self.page.locator("div[style='display:block'] label[class='required']").all_inner_texts()
        divs4_names=self.page.locator("label:visible[class='required']").all_inner_texts()
        divs4_loc=self.page.locator("label:visible[class='required']").all()
        divs4_locators=[]
        print(divs4_names)
        print(len(divs4_names))

        divs42_locators=[]
        for loc in divs4_loc:
            divs42_locators.append({"name":loc.inner_text(),
                                    "for":loc.get_attribute("for"),
                                    "locator":self.page.locator("#"+loc.get_attribute("for")),
                                  })
            

        print(divs42_locators)
        
        
        for name in divs4_names:
            if "imagen" not in name.lower():
                loc_list=self.page.get_by_label(name,exact=True).all()
                found_loc=get_first_enabled_locator(loc_list)
                divs4_locators.append({"name":name,
                                    #"locator":self.page.get_by_label(name,exact=True).locator()
                                    "locator":found_loc
                                    #locator:self.page.locator()
                                    #"tag_name":self.page.get_by_label(name,exact=True).first.evaluate("element => element.nodeName")
                                    })
                
            else:
                print(name)
                print("Locators de imagen no añadidos a la lista de locators")
            
        
        
        print("Campos de la sección 4 :Caracteristicas de la Oferta")
        print(divs4_names)
        print("locators")
        print(divs4_locators)

        #Getting locators elements and attributes

        #self.add_tag_n_attributes(divs4_locators)
        self.add_tag_n_attributes(divs4_locators)

        self.get_options_locator_list2(divs4_locators)


        #Getting options for aria-owns elements

        print("Imprimiendo opciones...")
        for loc in divs4_locators:
            print(loc["name"]+"-"+loc["tag"])
            print(loc["options"])
 
       # print(divs4_locators)
        print("Se capturaron los campos obligatorios")
        print("Llenando los campos obligatorios...")
        self.test_locators_list(divs4_locators)
        

    def load_images(self):
        image_locators=self.page.locator("input:enabled[type='file'][required]").all()
        print("Cantidad de img a subir: "+str(len(image_locators)))
        for img_loc in image_locators:
            img_route_mac="/Users/macbook/Downloads/test.jpeg"
            #img_route_resized=r"C:\Users\risin\Downloads\imgTest\test_1_resized.jpg"
            #print("Convirtiendo imagen a 1000x1000...")
            #resize_image(img_route,img_route_resized)
            #print("Imagen convertida")
            print("Cargando imagen...")
            img_loc.set_input_files(img_route_mac)
            print("Imagen cargada")

    def confirm_product(self):
        print("Confirmando producto...")
        self.page.get_by_role("button",name=re.compile("Presentar para su aprobación", re.IGNORECASE)).click()
        #self.page.get_by_role("button", name=" Presentar para su aprobación").click()
        print("Producto confirmado")
        print("Añadiendo otro producto...")

    def load_product_name(self):
        #self.page.locator("input[id='nombreFormatterHelp']").fill("productName")
        self.page.get_by_role("textbox", name="Nombre").fill("productName")

    def load_description(self):
        #self.page.locator("input[id='nombreFormatterHelp']").fill("productName")
        properties={
                "name":"description1",
                "value":"23434"
            }
        #insertPropertiesToPage("div[class='ql-editor ql-blank']",properties,self.page)
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

if __name__ == "__main__":
    RIPmloader=multiLoaderRIP(2)
    RIPmloader.go_to_home()
    #number_products = int(input("Set number of products:"))
    number_products=1
    for i in range(number_products):
        print("Subiendo producto N-"+str(i)+"...")
        RIPmloader.add_product()
        RIPmloader.load_all_category()
        #RIPmloader.load_section2_product_char()
        #RIPmloader.fill_textbox()
        RIPmloader.load_section_offer_char()
        RIPmloader.load_images()
        RIPmloader.confirm_product()
    print("Se crearon "+str(number_products)+ " productos")
    print('--------')

