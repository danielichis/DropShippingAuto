import os
import traceback
from playwright.sync_api import sync_playwright,expect
import requests
from DropShippingAuto.src.utilsDropSh.readAmazon import get_product_in_amazon_carpet_parsed
from utils.jsHandler import insertPropertiesToPage
from random import randrange
from datetime import date,timedelta
from utils.managePaths import mp
from utils.manipulateDicts import dictManipulator
from utils.datesHandling import dateManag
from utils.randomUtils import randomInt
from utils.dinamicMassivArgsExtractions import get_ia_anwsers_extended
from DropShippingAuto.src.marketPlacesDestino.real_plaza.smartSelects import get_best_path_real_plaza_category
from utils.imgHandling.imgHandling import image_file_to_binary
import json
import time
homeRealPlaza="https://inretail.mysellercenter.com/#/dashboard"
import re


def letter_to_number_string(s):
    # Convert each letter to its corresponding number and join them into a string
    return ''.join(str(ord(char) - ord('a') + 1)  if char.isalpha() else char for char in s.lower())

class LoaderRealPlaza:
    def __init__(self,dataToLoad=None,page=None,context=None,p=None,sheetProductData=None,configSheetData=None):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
        self.sheetProductData=sheetProductData
        self.configDataSheet=configSheetData
        self.imagesLoadedUrl=[]
        self.variant_id=None
        self.allFielldsConfig=True
    def start_playwright(self):
        self.p = sync_playwright().start()
        user_dir=mp.get_current_chrome_profile_path()
        self.browser = self.p.chromium.launch_persistent_context(user_dir,headless=False,slow_mo=50)
        self.page=self.browser.new_page()

    def handle_login_real_plaza(self):
        self.cookies=self.page.context.cookies()
        if self.page.url.find("https://inretail.mysellercenter.com/#/dashboard")!=-1:
            print("Ya se encuentra logueado")
            self.token= self.page.evaluate("() => JSON.parse(sessionStorage['vue-session-key'])['token']")
            return
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
        #print(r.json())
        search_categories_response=r.json()
        #make get request to get categories with page.route
        print("Categoría buscada")
    def select_category_to_get_specifications(self):

        if self.dataToLoad["clasificacion"]!="sin clasificacion":
            classification=str(self.dataToLoad["clasificacion"])
        else:
            initialPrompt="Esta es la informacion estructurada de un un producto de Amazon, por favor cual seria la mejor clasificacion para este producto ? :"
            classification=initialPrompt+str(self.dataToLoad)

        self.real_plaza_category=get_best_path_real_plaza_category(classification)
        urlEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/specifications/"
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        params = {
        'sortOrder': 'asc',
        'sortBy': 'name.keyword',
        'from': '0',
        'size': '100',
        'isActive': 'true',
        'categoryId': self.real_plaza_category['id'],
        'isStockKeepingUnit': 'false',
             }
        r=self.page.request.get(urlEndpoint,headers=header,params=params)
        self.specificationsFields=r.json()
        self.requiredFields=[field for field in self.specificationsFields if field["isRequired"]==True]
        specificationsRespone=r.json()
        print("Categoría Seleccionada")
    def get_answers_from_specifications(self):
        list_of_fields=[]
        for field in self.specificationsFields:
            fieldToFill={}

            if field['description']==None:
                field['description']=field["name"]

            if field["isRequired"]==True or self.allFielldsConfig==True:
                if field["specificationFieldValues"]==[] or field["specificationFieldValues"]==None:
                    fieldToFill['name']=field['name']
                    fieldToFill['fieldType']="input"
                    fieldToFill['description']=field['description']
                    fieldToFill['options']=[]
                    fieldToFill['id']=field['id']
                else:
                    fieldToFill['name']=field['name']
                    fieldToFill['fieldType']="select"
                    fieldToFill['description']=field['description']
                    fieldToFill['options']=field["specificationFieldValues"]
                    fieldToFill['id']=field['id']
                list_of_fields.append(fieldToFill)
        answers=get_ia_anwsers_extended(str(self.dataToLoad),list_of_fields)
        #setting warrant string
        if "Garantía" in answers.keys():
           answers["Garantía"]['details']['AIResponse']['value']="7 días por defecto de fábrica."
        #
        self.answers=answers
    
    def get_about_this_item_str(self,number_paragraphs:int):
        if "Acerca del producto" in self.dataToLoad.keys():
            about_this_item_str=dictManipulator.dict_to_bp_w_paragraphs(self.dataToLoad["Acerca del producto"],number_paragraphs)
            return about_this_item_str
        else:
            return self.dataToLoad["Resumen de 2 a 3 parrafos separados por viñetas"]

    def get_description_str(self)->str:
        description_dict=self.dataToLoad['descripciones']
        #adding sku to description_dict dictionary
        sku_dict={"SKU":self.dataToLoad['sku']}
        sku_dict.update(description_dict)
        description_str=dictManipulator.dict_to_string_bp(sku_dict)
        return description_str  

    def get_numeric_field_answer(self,answer:str,isRequired:bool):
        try:
            numeric_answer=round(float(answer))
            isNumber=True
        except Exception as e:
            print(str(e))
            print(answer + " no es un número")
            isNumber=False

        print("Campo numerico requerido :"+str(isRequired))
        print("Valor es un string conteniendo un número :"+str(isNumber))
        
        if isRequired:
            if isNumber:
                return numeric_answer
            else:
                return 1
        else:
            if isNumber:
                return numeric_answer
            else:
                return ""
        
    def create_product_api(self):
        for element in self.specificationsFields:
            if element["isRequired"]==True or self.allFielldsConfig==True:
                anwserElementValue=self.answers[element["name"]]['details']['AIResponse']['value']
                fielTypeName=element["specificationFieldType"]["fieldTypeName"]
                if fielTypeName=="Texto" or fielTypeName=="Input":
                    element["specificationFieldValues"]=[{"value":anwserElementValue}]
                elif fielTypeName=="Radio" or fielTypeName=="CheckBox":
                    anwserElementId=self.answers[element["name"]]['details']['AIResponse']['fieldValueId']
                    element["specificationFieldValues"]=[{"fieldValueId":anwserElementId,"value":anwserElementValue,"isActive":True}]
                elif fielTypeName=="Número":
                    anwserElementValue=self.get_numeric_field_answer(anwserElementValue,element["isRequired"])
                    element["specificationFieldValues"]=[{"value":anwserElementValue}]
                else:
                    anwserElementId=self.answers[element["name"]]['details']['AIResponse']['fieldValueId']
                    element["specificationFieldValues"]=[{"fieldValueId":anwserElementId,"value":anwserElementValue,"isActive":True}]
            else:
                element["specificationFieldValues"]=[{"value":""}]
        description_str=self.get_description_str()
        about_this_item_str=self.get_about_this_item_str(4)
        
        string_description=about_this_item_str +"\n"+description_str
        json_data = {
        'id': None,
        'skus': [],
        'category': {
            'id': self.real_plaza_category['id'],
            'name': self.real_plaza_category['name'],
            'namePath': self.real_plaza_category['namePath'],
        },
        'brand': {
            'id': self.brand_to_set['id'],
            'name': self.brand_to_set['name'],
            'isActive': self.brand_to_set['isActive'],
        },
        'productSpecifications':self.specificationsFields,
        'marketplaces': [
            {
                'id': 'promart',
                'name': 'Promart',
                'accountName': 'promart',
                'active': True,
                'productCommission': None,
            },
            {
                'id': 'plazavea',
                'name': 'Plaza Vea',
                'accountName': 'plazavea',
                'active': True,
                'productCommission': None,
            },
            {
                'id': 'oechsle',
                'name': 'Oechsle',
                'accountName': 'oechsle',
                'active': True,
                'productCommission': None,
            },
            {
            "id": "realplaza",
            "name": "RealPlaza",
            "accountName": "realplaza",
            "active": True,
            "productCommission": None
            }
        ],
        'name': self.dataToLoad['titulos_generados']['real plaza'],
        'description': f'<p>{string_description}</p>',
    }
        r=self.page.request.post(
            "https://inretail.mysellercenter.com/sellercenter/api/v1/products/",
        headers={"Authorization":f"Bearer {self.token}","Content-Type":"application/json"},
        data=json_data)
        self.product_id=r.json()["id"]
        product_create_response=r.json()
        print(f"Producto creado:{self.product_id}")
    def load_images_api(self):
        path_files=os.path.join(mp.sku_folder_path,self.dataToLoad['sku'],"images","resized_1000x1000")
        imagesListFiles=os.listdir(path_files)
        filesToPost=[]
        dictFiles={}
        for image in imagesListFiles:
            fullPath=os.path.join(path_files,image)
            contentImage = image_file_to_binary(fullPath)
            file=('file',(image,contentImage,'image/jpeg'))
            dictFiles[image]=contentImage
            filesToPost.append(file)
        header={"Authorization":f"Bearer {self.token}"}
        urlEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/sku/{self.variant_id}/images"
        r = requests.post(
                        urlEndpoint,
                        headers=header,
                        files=filesToPost,
                            )
        self.imagesLoadedUrl=[image['imageUrl'] for image in r.json()]
        load_image_response=r.json()
        print("Imágenes cargadas")
    def make_json_to_variant(self):
        try:
            peso_gr=int(float(self.dataToLoad['Peso en Kg del envio'].replace("Kg",""))*1000)
        except:
            peso_gr=200
        defaulDimensions=[30,36,16]
        try:
            dimensions_cm=self.dataToLoad['Dimensiones del producto en cm'].replace("cm","").split("x")
            dimensions_cm[0]=int(float(dimensions_cm[0])*1)
            dimensions_cm[1]=int(float(dimensions_cm[1])*1)
            dimensions_cm[2]=int(float(dimensions_cm[2])*1)
        except:
            dimensions_cm=defaulDimensions
        self.json_variant_data = {
                    'id': None,
                    'price': {
                        'listPrice': str(self.sheetProductData['PRECIO LISTA MARKETPLACE']),
                        'price': str(self.sheetProductData['PRECIO FINAL MARKETPLACE']),
                        'priceValidFrom': dateManag.todayString,
                        'priceValidUntil': dateManag.twoYearsLaterfromNowString,
                    },
                    'dimension': {
                        'height': str(defaulDimensions[0]),
                        'width': str(defaulDimensions[1]),
                        'length': str(defaulDimensions[2]),
                        'cubicWeight': str(defaulDimensions[0]*defaulDimensions[1]*defaulDimensions[2]),
                        'weight': str(peso_gr),
                    },
                    'images': [],
                    'skuSpecifications': [],
                    #'upc': str(randomInt(100000,999999))+self.dataToLoad['sku'],
                    'upc': dateManag.todayStringWOHyphen,
                    'skuName': self.dataToLoad['titulos_generados']['real plaza'],
                    'status': 'PENDING_APPROVAL',
                }
        
        print(f"Json de variante creado para el producto :{self.product_id}")
    def variant_api(self,method):
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        if method=="create":
            urlEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/products/{self.product_id}/sku"
            self.make_json_to_variant()
        elif method=="update":
            urlEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/sku/{self.variant_id}"
            self.json_variant_data['images']=self.imagesLoadedUrl
        if method=="create":
            r=self.page.request.post(
                urlEndpoint,
                headers=header,
                data=self.json_variant_data)
            self.variant_id=r.json()["id"]
        elif method=="update":
            r=self.page.request.put(
                urlEndpoint,
                headers=header,
                data=self.json_variant_data)
        create_variant_response=r.json()
        print(f"Variante creada/actualizada:{self.variant_id} para el producto:{self.product_id}")
    def set_stock_api(self):
        urlStockEndpoint=f"https://inretail.mysellercenter.com/sellercenter/api/v1/sku/inventories/{self.variant_id}"
        json_data = {
                'totalQuantity': '50',
                'reservedQuantity': 0,
            }
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        
        r=self.page.request.put(
            urlStockEndpoint,
            headers=header,
            data=json_data)
        
        baseUrl="https://inretail.mysellercenter.com/#/catalog/details/"
        self.finalUrl=f"{baseUrl}{self.product_id}"
        self.upc=self.json_variant_data['upc']
        stock_response=r.json()
        print("Stock actualizado")
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
    def search_brand(self):
        urlEndpoint='https://inretail.mysellercenter.com/sellercenter/api/v1/brands'
        params = {
        'text': self.dataToLoad['Marca,proveedor o fabricante'],
        }
        header={"Authorization":f"Bearer {self.token}",
                "Content-Type":"application/json"}
        brands=self.page.request.get(urlEndpoint,headers=header,params=params)
        branded=False
        if self.dataToLoad['Marca,proveedor o fabricante'].upper()!="AMAZON":
            for brand in brands.json():
                if brand["name"].upper()==self.dataToLoad['Marca,proveedor o fabricante'].upper():
                    self.brand_to_set={"id":brand["id"],"name":brand["name"],"isActive":brand["isActive"]}
                    branded=True
                    break
        if not branded:
            self.brand_to_set={
                                "id": "biOrOY8Bi4M-DKCliT1Y",
                                "name": "GENÉRICO",
                                "isActive": False
                            }
        print(self.brand_to_set)
        print("Marca encontrada")
    def end_playwright(self):
        self.browser.close()
        self.p.stop()
        print("Playwright cerrado")
    def load_main_real_plaza(self):
        try:
            self.search_brand()
            self.select_category_to_get_specifications()   
            self.get_answers_from_specifications()
            self.create_product_api()
            self.variant_api("create")
            self.load_images_api()
            self.set_stock_api()
            self.status="CARGADO CORRECTAMENTE"
            tb="Ok"
        except Exception as e:
            print("Error en el proceso de carga en Real Plaza")
            self.status="ERROR"
            tb=traceback.format_exc()
            print(tb)
            self.finalUrl="-"
            self.upc="-"
        self.responseLoad={
            "sku":self.dataToLoad['sku'],
            "status":self.status,
            "url":self.finalUrl,
            "marketplace":"Real Plaza",
            "condition":"new",
            "log":tb,
            "fecha":time.strftime("%Y-%m-%d %H:%M:%S"),
            "upc":self.upc,
            "codigo variante":self.variant_id
                        }
if __name__ == "__main__":
    with open("dataToDownloadAndLoad.json","r") as f:
        sheetData=json.load(f)
    dataAmazonTest=get_product_in_amazon_carpet_parsed(sheetData['dataToLoad'][0]['SKU'])
    RPmloader=LoaderRealPlaza(dataToLoad=dataAmazonTest,sheetProductData=sheetData['dataToLoad'][0],configSheetData=sheetData['configData'])
    RPmloader.start_playwright()
    RPmloader.go_to_home()
    RPmloader.handle_login_real_plaza()
    RPmloader.load_main_real_plaza()
    RPmloader.end_playwright()
    
