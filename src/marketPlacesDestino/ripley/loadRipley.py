import traceback
from playwright.sync_api import sync_playwright,expect
from utils.embeddings.embeding import get_best_similarity_option,get_best_similarity_option2
from utils.jsHandler import insertPropertiesToPage
#from DropShippingAuto.src.utils.dinamySelections import search_best_option
#from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
#from DropShippingAuto.src.marketPlacesDestino.dinners.readAmazon import infoDinnersToLoad
from utils.dinamicMassivArgsExtractions_rip import get_dinamic_args_extraction,list_attributes_ff_in_json,list_attributes_nff_in_json,get_dinamic_args_extraction2,list_attributes_fields_in_json,get_dinamic_answer,dinamic_order_categories
from utils.managePaths import mp
from DropShippingAuto.src.marketPlacesDestino.ripley.StringHandling import extract_number_of_for,get_id_ul,get_first_enabled_locator,keyboard_delete_text,extract_words_regex,atomize_classification_wo_prepositions,remove_duplicates_preserve_order,format_url_with_encoded_values
import json
import time
import re
from random import randrange
from datetime import date,timedelta
from PIL import Image
from utils.manipulateDicts import dictConverter
import os
import ast

#from img_sizer1000x1000 import resize_image

#from DropShippingAuto.src.main import amazon_mkt_peruvians


homeRipley="https://ripleyperu-prod.mirakl.net/login"
market_dashboard='https://ripleyperu-prod.mirakl.net/marketplace-dashboard/'

class LoaderRipley:
    # def __init__(self,dataToLoad):
    #     self.dataToLoad=dataToLoad
    #     self.p = sync_playwright().start()
    #     user_dir=mp.get_current_chrome_profile_path()
    #     self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False)
    #     self.page=self.browser.new_page()

    def __init__(self,dataToLoad,page,context,p,sheetProductData,configSheetData):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
        self.sheetProductData=sheetProductData
        self.configDataSheet=configSheetData

    def start_playwright(self):
        #self.p = sync_playwright().start()
        #user_dir=mp.get_current_chrome_profile_path()
        #self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False,record_video_dir='videos/',slow_mo=50)
        #self.page=self.browser.new_page()
        pass
        
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
        #self.page.get_by_role("link", name="Añadir una oferta").click()
        #CREATING PRODUCT FROM 'PRECIOS Y EXISTENCIAS' MENU
        # self.page.get_by_role("button", name="Precios y existencias").click()
        # self.page.get_by_role("menuitem", name="Ofertas").click()
        # self.page.get_by_role("link", name="+ Añadir una oferta").click()
        #page3.get_by_role("link", name="+ Crear un producto").click()

    response_categories_dict=[]

    def get_ripley_categories_response2(self)->bool:
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        amazon_categories=contentProduct['clasificacion']
        if amazon_categories=="sin clasificacion":
            print("No hay clasificación en Amazon")
            print("Generando categoría con la API...")
            description_gen="lista de tipo de producto o posibles categorías específicas para el producto según el diccionario enviado (ejemplo: laptops,carteras,electronica,jabones,etc) en formato string entre comillas para el producto,mínimo 3 ,máximo 5,todo entre corchetes,"
            while(True): 
                try:
                    #generated_categories=get_dinamic_args_extraction2(options_type='options_0',content_product=str(contentProduct),fieldsFromMarketPlace=[{"name":description_gen,"locator":None,"options":[]}])[description_gen]
                    generated_categories=get_dinamic_answer(str(contentProduct),description_gen)
                    print(generated_categories)
                    product_categories=ast.literal_eval(generated_categories)
                except Exception as e:
                    print(str(e))
                    print("Error al generar categoría con la API")
                    print("Generando de nuevo")
                else:
                    break
            print("Se generaron categorías exitosamente")
            #product_categories=list(set(atomize_classification_wo_prepositions(generated_categories)))
        else:
            #Invirtiendo lista de amazon
            print("Se encontró clasificación")
            product_categories=amazon_categories[::-1]

        print(product_categories)
        #Going to product_offers page to obtain categories
        self.page.goto("https://ripleyperu-prod.mirakl.net/mmp/shop/catalog/template/configure?modelType=PRODUCTS_OFFERS")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("domcontentloaded")
        #Atomizando,quitando preposiciones y removiendo duplicados sin afectar el orden
        no_duplicates_categories=remove_duplicates_preserve_order(atomize_classification_wo_prepositions(product_categories))
        print(no_duplicates_categories)
        # print("Ordenando categorías con la API...")
        # gen_categories=dinamic_order_categories(str(contentProduct),no_duplicates_categories)
        print(no_duplicates_categories)
        #print("Transformando a lista de Python")
        #possible_categories=ast.literal_eval(gen_categories)
        possible_categories=[*product_categories,*no_duplicates_categories]
        self.possible_categories=possible_categories
        print(possible_categories)
        for category_value in possible_categories:
            encoded_category_value=format_url_with_encoded_values(category_value)
            url_petition=f"https://ripleyperu-prod.mirakl.net/mmp/private/catalog/hierarchy/search?search={encoded_category_value}&selectedLocale=es_PE&withRoot=false"
            print(url_petition)
            try:
                with self.page.expect_response(url_petition,timeout=12000) as response_info:
                    self.page.locator("input[name='filter']").fill(category_value)
                response=response_info.value
                response_categories_list=json.loads(response.text())
                if response.status==200:
                    if len(response_categories_list)>0:
                        print("Categorías encontradas")
                        self.selected_category_value=category_value
                        self.response_categories_list=response_categories_list
                        self.response_categories_dict.append({"category":category_value,"categories_list":response_categories_list})
                        print('Se añadieron categorías')
                else:
                    print("Petición no exitosa")
                    print("Probando con siguiente categoría")
                    continue
            except Exception as e:
                print(str(e))
                continue

        print("Categorías no encontradas")
        print("Llamando de nuevo a la funcion para generar categorías")
        self.get_ripley_categories_response()
        print("Generando categoria con API")
        return False


    def get_ripley_categories_response(self)->bool:
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        amazon_categories=contentProduct['clasificacion']
        if amazon_categories=="sin clasificacion":
            print("No hay clasificación en Amazon")
            print("Generando categoría con la API...")
            description_gen="lista de tipo de producto o posibles categorías específicas para el producto según el diccionario enviado (ejemplo: laptops,carteras,electronica,jabones,etc) en formato string entre comillas para el producto,mínimo 3 ,máximo 5,todo entre corchetes,"
            while(True): 
                try:
                    #generated_categories=get_dinamic_args_extraction2(options_type='options_0',content_product=str(contentProduct),fieldsFromMarketPlace=[{"name":description_gen,"locator":None,"options":[]}])[description_gen]
                    generated_categories=get_dinamic_answer(str(contentProduct),description_gen)
                    print(generated_categories)
                    product_categories=ast.literal_eval(generated_categories)
                except Exception as e:
                    print(str(e))
                    print("Error al generar categoría con la API")
                    print("Generando de nuevo")
                else:
                    break
            print("Se generaron categorías exitosamente")
            #product_categories=list(set(atomize_classification_wo_prepositions(generated_categories)))
        else:
            #Invirtiendo lista de amazon
            print("Se encontró clasificación")
            product_categories=amazon_categories[::-1]

        print(product_categories)
        #Going to product_offers page to obtain categories
        self.page.goto("https://ripleyperu-prod.mirakl.net/mmp/shop/catalog/template/configure?modelType=PRODUCTS_OFFERS")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("domcontentloaded")
        #Atomizando,quitando preposiciones y removiendo duplicados sin afectar el orden
        no_duplicates_categories=remove_duplicates_preserve_order(atomize_classification_wo_prepositions(product_categories))
        print(no_duplicates_categories)
        # print("Ordenando categorías con la API...")
        # gen_categories=dinamic_order_categories(str(contentProduct),no_duplicates_categories)
        print(no_duplicates_categories)
        #print("Transformando a lista de Python")
        #possible_categories=ast.literal_eval(gen_categories)
        possible_categories=[*product_categories,*no_duplicates_categories]
        self.possible_categories=possible_categories
        print(possible_categories)
        for category_value in possible_categories:
            encoded_category_value=format_url_with_encoded_values(category_value)
            url_petition=f"https://ripleyperu-prod.mirakl.net/mmp/private/catalog/hierarchy/search?search={encoded_category_value}&selectedLocale=es_PE&withRoot=false"
            print(url_petition)
            try:
                with self.page.expect_response(url_petition,timeout=12000) as response_info:
                    self.page.locator("input[name='filter']").fill(category_value)
                response=response_info.value
                response_categories_list=json.loads(response.text())
                if response.status==200:
                    if len(response_categories_list)>0:
                        print("Categorías encontradas")
                        self.selected_category_value=category_value
                        self.response_categories_list=response_categories_list
                        return True
                else:
                    print("Petición no exitosa")
                    print("Probando con siguiente categoría")
                    continue
            except Exception as e:
                print(str(e))
                continue

        print("Categorías no encontradas")
        print("Llamando de nuevo a la funcion para generar categorías")
        self.get_ripley_categories_response()
        print("Generando categoria con API")
        return False
        
        

    def make_ripley_categories_paths(self):
        
        categories_list=self.response_categories_list
        
        categories_paths_codes=[]
        categories_paths_lists=[]
        categories_paths_str=[]

        for categ_dict in categories_list:
            if categ_dict["children"]==False:
                categories_paths_codes.append(categ_dict['fullHierarchy'])

        print(categories_paths_codes)
        print("Intercambiando codigos por etiquetas en cada ruta...")

        for path in categories_paths_codes:
            print(path)
            categories_paths_lists.append(list(map(self.replace_code_for_label,path[1:])))

        categories_paths_lists=categories_paths_lists
        print("Rutas de categorías:")
        print(categories_paths_lists)

        for path in categories_paths_lists:
            categories_paths_str.append(" > ".join(path))
        print("String de rutas")
        print(categories_paths_str)


        categories_paths={
            "lists":categories_paths_lists,
            "strings":categories_paths_str
        }

        self.categories_paths=categories_paths
        
        print("Se crearon las rutas de categorías")
        
    def replace_code_for_label(self,category_code:str)->str:
        print(category_code)
        if category_code!='':
            for categ_dict in self.response_categories_list:
                if categ_dict["code"]==category_code:
                    category_label=categ_dict["label"]
                    print(category_label)
                    break
        else:
            category_label=""

        return category_label

    def get_optimal_categories_path(self):
        # last_categories=[category[-1]["similarity"] for category in self.all_category_paths]
        # print(last_categories)
        # print("work")
        #category_to_embed=self.selected_category_value
        print("Transformando el contenido del producto a string")
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        print(contentProduct)
        print("Usando el contenido del producto en Embeddings")
        #top_string_path=get_best_similarity_option(self.categories_paths["strings"],category_to_embed)
        top_string_path=get_best_similarity_option(self.categories_paths["strings"],str(contentProduct))
        print(top_string_path)
        top_categories_path=top_string_path.split(" > ")
        print(top_categories_path)
        return top_categories_path

    def add_product(self):
        #self.page.get_by_role("button", name="Precios y existencias").click()
        self.page.get_by_role("menuitem", name="Ofertas").click()
        self.page.get_by_role("link", name="+ Añadir una oferta").click()
        self.page.get_by_role("link", name="+ Crear un producto").click()
        print("pagina cargada")

    def select_category_fc_n_embbedings(self,category_dict:dict)->int:
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        cat_options_names=[option["name"] for option in category_dict["options"]]
        category_name=category_dict["name"]
        category_list=[category_dict]
        #Using Function Calling OpenAI API
        category_selected=get_dinamic_args_extraction2(options_type='options_1',content_product=str(contentProduct),fieldsFromMarketPlace=category_list)
        print(category_selected)
        funcCallingValue=category_selected[category_name]
        print("Valor retornado con Function Calling : "+funcCallingValue)
        #Using value returned from Function Calling to use Embeddings
        #optionToSelect=get_best_similarity_option(cat_options_names,funcCallingValue)
        embedding_top_result=get_best_similarity_option2(cat_options_names,funcCallingValue)
        return embedding_top_result
        # #optionScore=embedding_top_result["similarity"]
        # optionToSelect=embedding_top_result["optionName"]
        # print("Categoría retornada con Embeddings :"+optionToSelect)
        # #finding the index of the value returned from the embeddings
        # categNumb=cat_options_names.index(optionToSelect)
        # return categNumb
    
    def get_category_number(self,category_dict:dict,optionToSelect:str)->int:
        cat_options_names=[option["name"] for option in category_dict["options"]]
        categNumb=cat_options_names.index(optionToSelect)
        return categNumb


    def make_category_dict(self,category_div_order:int)->list:
        categories_list_locator=self.page.locator("div[class='select2-result-label']").all()
        categories_list=[]
        for category in categories_list_locator:
            categories_list.append({"name":category.inner_text(),"locator":category})

        if category_div_order==0:
            category_label="Categoría"
        else:
            category_label="Subcategoría "+str(category_div_order)

        category_dict={"name":category_label,"options":categories_list}

        print(categories_list)
        print(category_dict)
        return category_dict

    def load_all_category(self):
        cat_num=0
        category_path=[]
        while(True):
            next_locator=self.page.locator(f"#next{str(cat_num)}")
            #next_locator=self.page.locator("div[id='next"+str(cat_num)+"']")
            try:
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_load_state("load")
                self.page.wait_for_load_state("domcontentloaded")
                expect(next_locator.locator("div[class='input col-md-4 col-lg-4']").first).to_be_enabled()
                next_locator.locator("div[class='input col-md-4 col-lg-4']").first.click(timeout=10000)
                category_dict=self.make_category_dict(cat_num)
                categories_list=category_dict["options"]
                #Using embeddings to select the best category
                embedding_top_result=self.select_category_fc_n_embbedings(category_dict)
                #optionScore=embedding_top_result["similarity"]
                #optionToSelect=embedding_top_result["optionName"]
                categNumb=self.get_category_number(category_dict,embedding_top_result["optionName"])
                embedding_top_result["categNumber"]=categNumb
                print(embedding_top_result)
                #addSelectiontoRoute
                ####
                #Select a random category
                #categNumb=randrange(0,len(categories_list))
                print(categNumb)
                categories_list[categNumb]["locator"].click()
                category_path.append(embedding_top_result)
                print("Categoria seleccionada")
                time.sleep(2)
                cat_num+=1
            except Exception as e:
                print(e)
                print("Ultima categoria seleccionada")
                self.add_to_all_category_paths(category_path)
                print("ruta")
                print(self.all_category_paths)
                print("Se añadió la ruta de categorías")
                print("No hay más categorías por seleccionar")
                break
   
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state('domcontentloaded')
        self.page.wait_for_load_state('load')

        print("Se cargaron todas las categorías")

        if embedding_top_result["similarity"]<0.8:
            print("Se volverán a cargar las categorías")
            return False
        else:
            print("Se seleccionaron bien las categorías")
            return True


    def load_defined_categories(self,top_categories_path:list):
        cat_num=0
        while(True):
            next_locator=self.page.locator(f"#next{str(cat_num)}")
            #next_locator=self.page.locator("div[id='next"+str(cat_num)+"']")
            try:
                self.page.wait_for_load_state("networkidle")
                self.page.wait_for_load_state("load")
                self.page.wait_for_load_state("domcontentloaded")
                expect(next_locator.locator("div[class='input col-md-4 col-lg-4']").first).to_be_enabled()
                next_locator.locator("div[class='input col-md-4 col-lg-4']").first.click(timeout=5000)
                category_name=top_categories_path[cat_num]
                self.page.get_by_role("option", name=category_name, exact=True).click()
                print("Categoria seleccionada")
                cat_num+=1
            except Exception as e:
                print(e)
                print("Ultima categoria seleccionada")
                print("No hay más categorías por seleccionar")
                break
   
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_load_state('domcontentloaded')
        self.page.wait_for_load_state('load')

        print("Se cargaron todas las categorías")


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


    def get_new_options_from_combobox(self,combobox_locator,cgpt_answer:str='d'):
        print("Obteniendo nuevas opciones de combobox...")
        id_ul=combobox_locator["options_id"]
        print(id_ul)
        self.page.keyboard.type(cgpt_answer,delay=50)
        time.sleep(4)
        
        options_list_locator=self.page.locator(f"#{id_ul}").locator("li").all()
        print(options_list_locator)
        #combobox_locator["locator"].click()

        new_options=[]
        for item in options_list_locator:
            new_options.append({"name":item.inner_text(),
                                "locator":item})
            
        combobox_locator["options"]=new_options
        print("Nuevas opciones...")
        print([x["name"] for x in new_options])
        print("Opciones obtenidas")
        



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
                    hidden_label=self.page.locator("label:visible[for^='s2id']").filter(has_text=title).first
                    for_attribute=hidden_label.get_attribute("for")
                    id_ul=get_id_ul(for_attribute)
                    print(id_ul)
                    try:
                        combobox_locator=self.page.locator("div[class='input col-md-4 col-lg-4']").filter(has=self.page.locator(f"input:enabled[title='{title}']")).first
                        combobox_locator.click()
                        #cgpt_answer="d"
                        #self.page.keyboard.type(cgpt_answer,delay=200)
                        #time.sleep(2)
                        time.sleep(1)
                        self.page.wait_for_load_state("networkidle")
                        options_list_locator=self.page.locator(f"#{id_ul}").locator("li").all()

                        options=[]
                        for item in options_list_locator:
                            options.append({"name":item.inner_text(),
                                            "locator":item})
                        #getting id of unordered list of options with through the hidden label which contains the number in the id of the unordered list
                        #how to compute the string
                        #id for unordered list of results>s2-results-{number}
                        #will obtain the number from the id of the label ,the id in the label has the form s2id_autogen{number}

                    except Exception as e:
                        print("Error al hacer click en combobox"+str(e))
                        print("Pasando a siguiente elemento")
                        continue
                    #id=locator["key_values"]["aria-owns"]


                    print(id)
                    print([x["name"] for x in options])
                    #locator["combobox"]=combobox_locator
                    locator["options_id"]=id_ul
                    locator["options"]=options
                    #select first option 
                    locator["options"][0]["locator"].click()
                    #update locator with combobox locator
                    locator["locator"]=combobox_locator
                    #2ND click to close the combobox
                    #combobox_locator.click()
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
        #Separating list in fillable and options
        self.fields_fillable=[]
        self.fields_nonfillable=[]

        for loc in locators_list:
            print(loc["name"]+"-"+loc["tag"])
            if len(loc["options"])==0:
                try:
                    self.fields_fillable.append(loc)
                    if loc['name']=='Cantidad de la oferta' or loc['name']=='Precio':
                        loc["locator"].fill("25")
                    else:
                        loc["locator"].fill("TEST MODAFUCKAAAA")
                        
                except Exception as e:
                    print("error"+str(e))
                    print("Pasando a siguiente elemento")
                    continue
            else:
                self.fields_nonfillable.append(loc)
                categNumb=randrange(0,len(loc["options"]))
                print(categNumb)
                if loc["tag"]=="SELECT":
                    option_label=loc["options"][categNumb]["name"]
                    loc["locator"].select_option(label=option_label)
                elif loc["tag"]=="INPUT":
                    loc["locator"].click()
                    #cgpt_answer="something"
                    #self.page.keyboard.type(cgpt_answer,delay=150)
    #                   page1.get_by_role("link", name="100%").click()
    # page1.get_by_role("option", name="1976 NATURAL PRODUCTS").click()
    # page1.get_by_role("link", name="1976 NATURAL PRODUCTS").click()
    # page1.get_by_role("combobox", name="Marca").fill("er")
    # page1.get_by_role("option", name="29 SUPER FOODS").click()
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


    def test_locators_list2(self,locators_list:list)->None:
        #Separating list in fillable and options
        self.fields_fillable=[]
        self.fields_nonfillable=[]

        for loc in locators_list:
            print(loc["name"]+"-"+loc["tag"])
            if len(loc["options"])>0:
                self.fields_nonfillable.append(loc)
                categNumb=randrange(0,len(loc["options"]))
                print(categNumb)
                if loc["tag"]=="SELECT":
                    option_label=loc["options"][categNumb]["name"]
                    loc["locator"].select_option(label=option_label)
                elif loc["tag"]=="INPUT":
                    loc["locator"].click()
                    #cgpt_answer="something"
                    #self.page.keyboard.type(cgpt_answer,delay=150)
    #                   page1.get_by_role("link", name="100%").click()
    # page1.get_by_role("option", name="1976 NATURAL PRODUCTS").click()
    # page1.get_by_role("link", name="1976 NATURAL PRODUCTS").click()
    # page1.get_by_role("combobox", name="Marca").fill("er")
    # page1.get_by_role("option", name="29 SUPER FOODS").click()
                    loc["options"][categNumb]["locator"].click()
                print("Element selected")
            else:
                try:
                    
                    if loc['name']=='Cantidad de la oferta':
                        loc["locator"].fill("0")
                    elif loc['name']=='Precio':
                        loc["locator"].fill("1")
                    #elif loc['name']=='Nombre':
                    #    loc['name']='Nombre,máximo 129 caracteres'    
                    else:
                        loc["locator"].fill("TEST MODAFUCKAAAA")

                    self.fields_fillable.append(loc)
                        
                except Exception as e:
                    print("error"+str(e))
                    print("Pasando a siguiente elemento")
                    continue

        print("Se seleccionaron elementos")   


    def split_required_fields(self)->None:
        #Separating list in fillable and non fillable fields
        locators_list=self.required_fields
        print("////////////")
        print("Separando campos a llenar en con y sin opciones...")
        self.fields_fillable=[]
        self.fields_nonfillable=[]

        for loc in locators_list:
            print(loc["name"]+"-"+loc["tag"])
            if len(loc["options"])>0:
                print("Campo sin opciones")
                self.fields_nonfillable.append(loc)
            else:
                print("Campo con opciones")
                self.fields_fillable.append(loc)

        print("Se separaron los campos a llenar en campos con opciones y campos sin opciones")
        print("////////////")   

        
    def get_all_required_fields(self):

        divs4_names=self.page.locator("label:visible[class='required']").all_inner_texts()
        divs4_loc=self.page.locator("label:visible[class='required']").all()
        divs4_locators=[]
        print(divs4_names)
        print(len(divs4_names))

        # divs42_locators=[]
        # for loc in divs4_loc:
        #     divs42_locators.append({"name":loc.inner_text(),
        #                             "for":loc.get_attribute("for"),
        #                             "locator":self.page.locator("#"+loc.get_attribute("for")),
        #                           })
            

        # print(divs42_locators)
        
        
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
        #print("Llenando los campos obligatorios...")
        #self.test_locators_list2(divs4_locators)
        self.required_fields=divs4_locators

    def resizing_images(self)->list:
        ripleyCustomSize=(750,555)
        imgDirectory=os.path.dirname(self.dataToLoad["imagesPath"][0])
        ripleyFolderDir=os.path.join(imgDirectory,"ripley750x555")
        resizedImgPaths=[]
        os.makedirs(ripleyFolderDir,exist_ok=True)
        print(imgDirectory)
        for i,resizedImg in enumerate(self.dataToLoad["imagesPath"]):
            print("Redimensionando imagen : "+resizedImg+str(i+1))
            ripImg=Image.open(resizedImg)
            ripImg.thumbnail(ripleyCustomSize,Image.Resampling.LANCZOS)
            #ripImg=ripImg.resize(ripleyCustomSize)
            ripley_image_path=os.path.join(ripleyFolderDir,f"resizedImg_ripley_{i}.jpg")
            ripImg.save(ripley_image_path)
            print("Imagen redimensionada"+str(i+1))
        print("Se redimensionaron imágenes")

        #get routes of resized images
        for image in os.listdir(ripleyFolderDir):
            if os.path.splitext(image)[1] == '.jpg':
                resizedImgPaths.append(os.path.join(ripleyFolderDir,image))

        print(resizedImgPaths)
        return resizedImgPaths

    def load_images(self):
        print("Redimensionando imágenes...")
        resizedImgPaths=self.resizing_images()
        image_locators=self.page.locator("input:enabled[type='file']").all()
        number_loadable_images=min(len(resizedImgPaths),len(image_locators))
        print("Cantidad de img a subir: "+str(number_loadable_images))
        for i in range(number_loadable_images):            
            print("Cargando imagen "+str(i+1)+"...")
            if i<2:
                image_locators[i].set_input_files(resizedImgPaths[0])
            else:
                image_locators[i].set_input_files(resizedImgPaths[i])
            print("Imagen cargada")
        print("Se cargaron todas las imágenes")

    def print_split_fields(self):
        print("Fillable Fields")
        print([x["name"] for x in self.fields_fillable])
        print("-------------------")
        print("Nonfillable Fields")
        for field in self.fields_nonfillable:
            print(field["name"])
            print([x["name"] for x in field["options"]])
        print("-------------------")


    def confirm_product(self):
        print("Confirmando producto...")
        self.page.get_by_role("button",name=re.compile("Presentar para su aprobación", re.IGNORECASE)).click()
        print("Producto confirmado")
        print("Añadiendo otro producto...")

    def load_description(self)->str:
        description=self.dataToLoad['descripciones']
        description_str=dictConverter().dict_to_string_bp(description)
        #self.page.locator("#productAndOffersCommand-attributeValuesFormCommand-1103").fill("---")
        #self.page.locator("#productAndOffersCommand-attributeValuesFormCommand-1103").fill(description_str)
        return description_str
        #self.page.locator("#productAndOffersCommand-attributeValuesFormCommand-1103").type("---")
        #print("Descripción cargada")

    def load_package_dimensions(self,alto:int,ancho:int,largo:int):
        print("Cargando dimensiones del paquete...")
        self.page.get_by_role("textbox", name="alto empaque *").fill(str(alto))
        self.page.get_by_role("textbox", name="ancho empaque *").fill(str(ancho))
        self.page.get_by_role("textbox", name="largo empaque *").fill(str(largo))

        print("Dimensiones del paquete cargadas")


    def fill_fillable_fields(self):
        #self.static_filled_fields=['Descripcion','Precio','largo empaque','alto empaque','ancho empaque']
        self.static_filled_fields=['Precio','largo empaque','alto empaque','ancho empaque']
        print("Llenando campos sin opciones con información del producto...")
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        dimArgs=get_dinamic_args_extraction2(options_type="options_0",content_product=str(contentProduct),fieldsFromMarketPlace=self.fields_fillable)
        print(dimArgs)
        for field in self.fields_fillable:
            textField=field["name"]
            
            if textField in self.static_filled_fields:
                print(f"Campo {textField}  se llenó sin uso de la API")
                print("Pasando a siguiente campo")
                continue
            elif textField=='Descripcion':
                static_description=self.load_description()
                valueField=dimArgs['Descripción Corta'] + "\n"+ static_description        
            elif textField=='sku_seller':
                valueField=self.product_sku
            elif textField=='Nombre':
                    valueField=dimArgs['Nombre'] if len(dimArgs['Nombre'])<=129 else self.generate_dinamic_answer("Nombre resumido en máximo 129 caracteres incluyendo espacios en blanco")
            elif textField=='Descripción Corta':
                print("generando Descripcion corta...")
                #valueField=dimArgs['Descripción Corta'] if len(dimArgs['Descripción Corta'])<=180 else self.generate_dinamic_answer("Descripción corta resumida en máximo 180 caracteres incluyendo espacios en blanco")
                short_name=dimArgs["Nombre"]
                short_header="Compra tu "+" en Ripley Internacional"
                max_chars=129-len(short_header)
                if len(short_name)>max_chars:
                    print("Generando nuevo nombre corto para la Descripción corta porque excede el límite de caracteres")
                    new_name_constraints="Nombre,"+f"no sobrepasar los {str(max_chars)} caracteres incluyendo espacios en blanco"
                    print(new_name_constraints)
                    while(True):
                        short_name=get_dinamic_args_extraction2(options_type="options_0",content_product=str(contentProduct),fieldsFromMarketPlace=[{"name":new_name_constraints,"locator":None,"options":[]}])[new_name_constraints]
                        short_description="Compra tu "+short_name+" en Ripley Internacional"
                        print(short_description)
                        if len(short_description)<=129:
                            break
                        else:
                            print("Generando nuevo nombre corto para la Descripción corta porque excede el límite de caracteres")
                else:
                    short_description="Compra tu "+short_name+" en Ripley Internacional"
                valueField=short_description
            elif textField=='Cantidad de la oferta':
                valueField='0'
            elif textField=='Peso (kg)':
                valueField=dimArgs['Peso (kg)'] if dimArgs['Peso (kg)']!="" and dimArgs['Peso (kg)']!="No Especifica" else "N/A"
            elif textField=='Precio':
                #valueField=self.load_base_price()
                continue
            else:
                valueField=dimArgs[textField]
                if valueField=="":
                    print("Llenando campo porque se retornó vacío : "+textField)
                    #print("Generando valor para porque está vacío:"+textField)
                    #valueField=self.generate_dinamic_answer(textField)
                    valueField="No especificado"
            
            field["locator"].fill(valueField)
            print("Se llenó :" + field["name"])#+"-"+valueField)
        print("Campos sin opciones llenados")

    def fill_nonfillable_fields(self):
        print("Llenando campos con opciones con información del producto...")
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        dimArgs=get_dinamic_args_extraction2(options_type="options_1",content_product=str(contentProduct),fieldsFromMarketPlace=self.fields_nonfillable)
        print(dimArgs)

        for field in self.fields_nonfillable:
            textField=field["name"]
            valueField=dimArgs[textField]
            print("Llenando campo :"+textField)
            print(valueField)

            if field["tag"]=="SELECT":
                option_label=valueField
                field["locator"].select_option(label=option_label)
            elif field["tag"]=="INPUT":

                field["locator"].click()
                try:
                    self.get_new_options_from_combobox(field,cgpt_answer=valueField)
                    if len(field["options"])==1:
                        if field["options"][0]["name"]=="No se encontraron resultados":
                            print("No se encontraron resultados")
                            keyboard_delete_text(self.page,valueField)

                            if textField=="Marca":
                                self.page.keyboard.type("unaluka")
                            else:
                                valueField_words=extract_words_regex(valueField)
                                self.page.keyboard.type(valueField_words[0])
                                #Sinonimos
                                #buscar de nuevo
                                #bucle,funcion recursiva quizás
                                pass
                            self.page.wait_for_load_state("networkidle")
                            time.sleep(2)
                            self.page.keyboard.press("Enter")
                        else:
                            self.page.wait_for_load_state("networkidle")
                            time.sleep(2)
                            self.page.keyboard.press("Enter")
                    else:
                        print("Se encontraron resultados")
                        optionToSelect=get_best_similarity_option([x["name"] for x in field["options"]],valueField)
                        print(optionToSelect)
                        categNumb=[x["name"] for x in field["options"]].index(optionToSelect)
                        field["options"][categNumb]["locator"].click()
                    #capture_options
                    #if options=No se encontraron resultados
                    #select unaluka ,for marca
                    #other cases 
                    #select first option with embeddings 
                except Exception as e:
                    print("ERROR INTERNO "+str(e))
                    self.page.keyboard.press("Enter")

        print("Campos con opciones llenados")



    def fill_nonfillable_fields2(self):
        print("Llenando campos con opciones con información del producto...")
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        dimArgs=get_dinamic_args_extraction2(options_type="options_1",content_product=str(contentProduct),fieldsFromMarketPlace=self.fields_nonfillable)
        print(dimArgs)

        for field in self.fields_nonfillable:
            textField=field["name"]
            valueField=dimArgs[textField]
            print("Llenando campo :"+textField)
            print(valueField)
            if field["tag"]=="SELECT":
                option_label=valueField
                try:
                    field["locator"].select_option(label=option_label,timeout=10000)
                except:
                    if textField=="Condición":
                        print("No se encontró información respecto a la condición del producto")
                        print("Seleccionando <<Nuevo>> como opción por defecto")
                        option_label="Nuevo"
                        field["locator"].select_option(label=option_label)                    
                    else:
                        print("Error al seleccionar opción tipo select : "+textField )
                        print("Pasando a siguiente campo")
                        continue
            elif field["tag"]=="INPUT":
                field["locator"].click()
                try:
                    self.search_best_option_combobox(field,textField,valueField,valueField)
                except Exception as e:
                    print("ERROR INTERNO "+str(e))
                    self.page.keyboard.press("Enter")
                    #raise Exception("No se encontraron resultados")

        print("Campos con opciones llenados")

    ####counter for the amount of times to find the best option in the combobox
    combobox_search_counter=-1
    #######

    def search_best_option_combobox(self,combobox_locator,textField:str,valueField:str,valueToSearch=None)->str:
        
        field=combobox_locator   
        print("campo recibido : "+textField)
        self.get_new_options_from_combobox(field,cgpt_answer=valueField if valueToSearch==None else valueToSearch)   
        if len(field["options"])==1:
            if field["options"][0]["name"]=="No se encontraron resultados":
                print("No se encontraron resultados")
                keyboard_delete_text(self.page,word_to_erase=valueField if valueToSearch==None else valueToSearch)
                print("Seleccionando opciones por defecto...")
                if textField=="Marca":
                    self.page.keyboard.type("UNALUKA")
                    #self.page.keyboard.type("GENÉRICO")
                    self.page.wait_for_load_state("networkidle")
                    time.sleep(2)
                    self.page.keyboard.press("Enter")
                elif textField=="Color":
                    self.page.keyboard.type("Multicolor")
                    self.page.wait_for_load_state("networkidle")
                    time.sleep(2)
                    self.page.keyboard.press("Enter")
                elif textField=="Tipo de producto":
                    self.combobox_search_counter+=1
                    print("Enriqueciendo la lista de categorias")
                    valueField_words=[*atomize_classification_wo_prepositions(valueField),*self.possible_categories]
                    print(valueField_words)
                    #recursive
                    if self.combobox_search_counter<len(valueField_words):
                        print("Buscando la mejor opcion para el combobox "+ str(self.combobox_search_counter+1)+"° vez")
                        print(valueField_words[self.combobox_search_counter])
                        self.search_best_option_combobox(field,textField,valueField,valueField_words[self.combobox_search_counter])
                    else:
                        self.combobox_search_counter=-1
                        print("No se encontraron resultados")
                        raise Exception("No se encontraron resultados para el combobox tipo de Producto")           

                else:
                    self.combobox_search_counter+=1
                    valueField_words=atomize_classification_wo_prepositions(valueField)
                    #recursive
                    if self.combobox_search_counter<len(valueField_words):
                        print("Buscando la mejor opcion para el combobox "+ str(self.combobox_search_counter+1)+"° vez")
                        print(valueField_words[self.combobox_search_counter])
                        self.search_best_option_combobox(field,textField,valueField,valueField_words[self.combobox_search_counter])
                    else:
                        self.combobox_search_counter=-1
                        print("No se encontraron resultados")
                        raise Exception("No se encontraron resultados para el comboBox")
                    #Sinonimos
                    #buscar de nuevo
                    #bucle,funcion recursiva quizás 
            else:
                self.page.wait_for_load_state("networkidle")
                time.sleep(2)
                self.page.keyboard.press("Enter")
                self.combobox_search_counter=-1
        else:
            print("Se encontraron resultados")
            options_name_list=[x["name"] for x in field["options"]]
            optionToSelect=get_best_similarity_option(options_name_list,valueField)
            print("opcion seleccionada : "+ optionToSelect)
            categNumb=options_name_list.index(optionToSelect)
            field["options"][categNumb]["locator"].click()
            self.page.wait_for_load_state("networkidle")
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_load_state("load")
            self.combobox_search_counter=-1
            time.sleep(2)
 
    def raise_test_error(self):
        raise Exception("--------<<<<Test Error>>>>----------")

    def load_offer_settings(self):
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        self.product_info=contentProduct
        self.product_sku=contentProduct["sku"]
        print(self.product_sku)
        #filling offer sku field
        self.page.get_by_label("SKU de oferta").fill(self.product_sku)
        #filling offer periods until 2028
        self.page.get_by_label("Período de descuento").click()
        self.page.get_by_role("button", name="Hoy").click()
        self.page.get_by_role("button", name="Cerrar").click()
        self.page.locator("#ui-id-0runningPricing-discountValidityInterval-end").fill("31/12/2030 00:00")
        self.page.get_by_role("button", name="Cerrar").click()
        print("Se llenaron los parámetros de la oferta")

    def generate_dinamic_answer(self,field_to_gen:str)->str:
        contentProduct=mp.data_sku(self.dataToLoad['sku'])
        #print(contentProduct)
        generated_field=get_dinamic_answer(content_product=str(contentProduct),field_to_generate=field_to_gen)
        print("--------------")
        print(field_to_gen+' : '+generated_field)
        print("--------------")
        #return {"name":field_to_gen,"value":generated_field}
        return generated_field
        
    def load_base_price(self):
        base_price=str(self.sheetProductData['PRECIO LISTA MARKETPLACE'])
        self.page.get_by_label("Precio", exact=True).fill(base_price)
        
    def load_special_price(self):
        special_price=str(self.sheetProductData['PRECIO FINAL MARKETPLACE'])
        self.page.get_by_label("Precio con descuento").fill(special_price)

    def load_model_number(self):
        content_product=mp.data_sku(self.dataToLoad['sku'])
        field_to_extract="Número de modelo.No es el SKU ni el ASIN"
        model_number=get_dinamic_args_extraction2(options_type="options_0",content_product=str(content_product),fieldsFromMarketPlace=[{"name":field_to_extract,"locator":None,"options":[]}])[field_to_extract]
        print(model_number)
        if model_number!= self.dataToLoad['sku']:
            self.page.get_by_role("textbox", name="Modelo").fill(model_number)

    def load_sku(self):
        print('--------')
        print("Cargando SKU..."+self.dataToLoad['sku'])
        wereCategoriesFound=self.get_ripley_categories_response()
        if wereCategoriesFound:
            self.make_ripley_categories_paths()
            top_categories_path=self.get_optimal_categories_path()
            self.add_product()
            #for i in range(1):
            #
            #isGoodSelection=False
            #while(not isGoodSelection):
                #isGoodSelection=self.load_all_category()
            self.load_defined_categories(top_categories_path)
            self.get_all_required_fields()
            self.split_required_fields()
            self.load_offer_settings()
            #self.load_description()
            self.load_images()
            self.load_base_price()
            self.load_special_price()
            self.load_model_number()
            self.load_package_dimensions(30,36,16)
            self.print_split_fields()
            self.fill_fillable_fields()
            self.fill_nonfillable_fields2()
            #self.generate_dinamic_answer("Descripción")
            #self.generate_dinamic_answer("Descripción corta")
            #self.confirm_product()
            print("//////////////////Producto cargado////////////////////////")
            print("Se creó producto con SKU: "+self.dataToLoad['sku'])
            print('--------')
            self.raise_test_error()
        else:
            print("No se encontraron categorías")
            raise Exception("No se encontraron categorías")

    def load_main_ripley(self):
        try: 
            self.load_sku()   
        except Exception as e:
            tb=traceback.format_exc()
            print("Error:"+str(e))
            print(str(tb))
            print("Error al cargar producto")
            print("Retornando a la página principal...")
            self.page.goto(market_dashboard)
            self.page.get_by_role("link", name="Añadir una oferta").click()
            print("Cargando otro producto...")



if __name__ == "__main__":

    # with open("dataToDownloadAndLoad.json","r") as f:
    #     sheetData=json.load(f)
    # print("cargando productosSS")
    # #amp=amazon_mkt_peruvians(sheetData)
    # #amp.main_process()
    # RIPloader=LoaderRipley(2)
    # RIPloader.start_playwright()
    # RIPloader.go_to_home()
    # #number_products = int(input("Set number of products:"))
    # number_products=1
    # for i in range(number_products):
    #     print("Subiendo producto N-"+str(i)+"...")
    #     RIPloader.add_product()
    #     RIPloader.load_all_category()
    #     #RIPmloader.load_section2_product_char()
    #     #RIPmloader.fill_textbox()
    #     RIPloader.load_section_offer_char()
    #     RIPloader.load_images()
    #     RIPloader.print_split_fields()
    #     RIPloader.confirm_product()
    # print("Se crearon "+str(number_products)+ " productos")
    # print('--------')

    for i in range(5,2,-1):
        print(i)

