
from playwright.sync_api import sync_playwright
import time
import traceback
from DropShippingAuto.src.marketPlacesDestino.shopify.interfaces import productosShopify as pshopy
from DropShippingAuto.src.marketPlacesDestino.shopify.interfaces import acfMetafields as acm
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from DropShippingAuto.src.utilsDropSh.readAmazon import get_product_in_amazon_carpet_parsed
from DropShippingAuto.src.utilsDropSh.managePaths import dictManipulator
from DropShippingAuto.src.utilsDropSh.dinamySelections import search_best_option
from utils.dinamicMassivArgsExtractions_rip import get_dinamic_answer,dinamic_two_systems_description
from utils.dinamicMassivArgsExtractions import dinamic_two_systems_description_dict,dinamic_title_per_mkp
from utils.manipulateDicts import dictManipulator
from utils.embeddings.embeding import get_top_n_match
from utils.embeddings.embeding import get_best_category_shopify
import json
import re
import os
from utils.jsHandler import insertPropertiesToPage

class LoaderShopify:
    def __init__(self,dataToLoad,sheetProductData,configSheetData,page,context,p):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
        self.sheetProductData=sheetProductData
        self.configDataSheet=configSheetData
        self.status="ERROR AL CARGAR"
    def load_descriptions(self):
        descs=self.dataToLoad['descripciones']
        if type(descs)!=dict:
            raise Exception("el parametro descs debe ser un diccionario")
        listaObjetos=[]
        listaObjetos.append({
            "campo":"SKU",
            "valor":": "+self.dataToLoad['sku']
        })
        for k,v in descs.items():
            listaObjetos.append({
                "campo":k.replace("'","").replace('"',""),
                "valor":": "+v.replace("'","").replace('"',"")
            })
        #description_str=dinamic_two_systems_description(dictManipulator.dict_to_string_bp(descs))
        self.page.frame_locator(pshopy.frameDescripcionProducto.selector).locator(pshopy.cajaDescripcionProducto.selector).click()
        diccionario=str(listaObjetos)
        codigo_js="var box=document.querySelector('iframe[id=product-description_ifr]').contentDocument.querySelector('body');var lista=document.createElement('ul');var listaDeObjetos = %s;for (const objeto of listaDeObjetos){var pelem=document.createElement('li');var stronge=document.createElement('strong');var valor=document.createTextNode(objeto.valor);stronge.textContent=objeto.campo;pelem.appendChild(stronge);pelem.appendChild(valor);lista.appendChild(pelem)};box.appendChild(lista);" %(diccionario)
        self.page.evaluate(codigo_js)

    def load_shopify_category_suggestion(self):
        try:
            self.page.query_selector("input[name='productType']").click(timeout=3000)
            aria_attribute=self.page.query_selector("input[name='productType']").get_attribute("aria-controls")
            #list_categories=self.page.locator("div[id='%s'] ul>li" %(aria_attribute)).all_inner_texts()
            list_categories=self.page.locator("ul[id='%s']>li" %(aria_attribute)).all_inner_texts()
            categorieToSelect=get_best_category_shopify(self.dataToLoad['clasificacion'],list_categories,useSavedEmbeds=False)
            selector="ul[id='%s']>li:has-text('%s')" %(aria_attribute,categorieToSelect)
            self.page.locator(selector).click(timeout=3000)
        except:
            pass

    def select_shopify_collections(self):
        amazonDatSku=self.dataToLoad
        self.page.locator("input[id='CollectionsAutocompleteField1']").click()
        currentCollections=self.page.locator("ul[aria-labelledby='CollectionsAutocompleteField1Label'] li span div").all_inner_texts()
        TopCollections=get_top_n_match(amazonDatSku,currentCollections,3)
        #Añadiendo coleccion Lo Nuevo Unaluka por defecto a la lista de colecciones
        TopCollections.append({'collecion': 'Lo Nuevo Unaluka', 'similarity': "Seleccionado por defecto"})
        #self.page.select_option("Colecciones",name="Colecciones")
        #self.page.locator("div:has(>ul[aria-labelledby='CollectionsAutocompleteField1Label'])").scroll_into_view_if_needed()    
        for collection in TopCollections:
            #self.page.get_by_role("combobox", name="Colecciones").fill()
            try:
                self.page.get_by_role("option", name=collection['collecion'],exact=True).locator("div").nth(1).click(timeout=3000)
            except Exception as e:
                tb=traceback.format_exc()
                print(tb)
                pass
            #page_shopi.locator(f"//span/div[text()={collection['collecion']}]").click()
            #page_shopi.get_by_role("combobox", name="Colecciones").fill("")
    def load_main_sku_shopify(self):
        try:
            url=self.load_sub_main_shopify()
            tb="ok"
            self.status="CARGADO CORRECTAMENTE"
        except Exception as e:
            tb=traceback.format_exc()
            url=""
        responseLoad={
            "sku":self.dataToLoad['sku'],
            "status":self.status,
            "url":url,
            "marketplace":"shopify",
            "condition":"new",
            "log":tb,
            "fecha":time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(responseLoad)
        with open("DropShippingAuto/Responsedata_load_shopify.json","w",encoding="utf-8") as json_file:
            json.dump(responseLoad,json_file,indent=4,ensure_ascii=False)
        self.responseShopifyLoad=responseLoad
    def load_provider(self):
        self.page.locator("input[name='vendor']").click()
        key=self.page.locator("input[name='vendor']").get_attribute("aria-controls")
        selectorProviders="ul[id='%s']>li>div>div>div" %(key)
        ulElementSelector="ul[id='%s']" %(key)
        list_providers=self.page.locator(selectorProviders).all_inner_texts()
        wildcardBrand="Genérico"

        # if "Marca" in self.dataToLoad.keys():
        #     if self.dataToLoad['Marca']!="No especificado":
        #         provider=self.dataToLoad['Marca']
        #         if provider in list_providers:
        #             self.page.locator(ulElementSelector).get_by_label(provider).all()[0].click()
        #         else:
        #             self.page.locator(ulElementSelector).get_by_label(wildcardBrand).all()[0].click()
        #     else:
        #         self.page.locator(ulElementSelector).get_by_label(wildcardBrand).all()[0].click()
        # else:
        #     self.page.locator(ulElementSelector).get_by_label(wildcardBrand).all()[0].click()
        provider=self.dataToLoad["Marca,proveedor o fabricante"]
        #provider="TESTMARCA"
        if provider.upper()!="NO ESPECIFICA":
            if provider in list_providers:
                self.page.locator(ulElementSelector).get_by_label(provider).all()[0].click()
            else:
                self.page.locator("input[name='vendor']").fill(provider)
        else:
            self.page.locator(ulElementSelector).get_by_label(wildcardBrand).all()[0].click()


    def load_title(self):
        self.page.wait_for_selector(pshopy.cajaNombreProducto.selector)
        #cambiar a un iframe
        self.page.query_selector(pshopy.cajaNombreProducto.selector).fill(self.dataToLoad["titulos_generados"]["shopify"])
    
    def load_images(self):
        self.page.wait_for_selector("span>input[type='file']")
        self.page.locator("span>input[type='file']").set_input_files(self.dataToLoad['imagesPath']['1000x1000'])
        pass
    def load_prices(self):
        self.page.wait_for_selector(pshopy.cajaPrecioProducto.selector)
        self.page.locator(pshopy.cajaPrecioProducto.selector).click()
        self.page.locator(pshopy.cajaPrecioProducto.selector).fill(str(self.sheetProductData['PRECIO FINAL MARKETPLACE']),timeout=3000)
        self.page.locator(pshopy.cajaPrecioComparacion.selector).click()
        self.page.locator(pshopy.cajaPrecioComparacion.selector).fill(str(self.sheetProductData['PRECIO LISTA MARKETPLACE']),timeout=3000)
    
    def load_stock(self):
        self.page.locator(pshopy.cajaStock.selector).click()
        self.page.locator(pshopy.cajaStock.selector).fill("50")
    
    def load_sku(self):
        self.page.locator(pshopy.cajaSKU.selector).click()
        self.page.locator(pshopy.cajaSKU.selector).fill(self.dataToLoad['sku'])
    
    def load_peso(self):
        self.page.locator(pshopy.cajaPesoDelProducto.selector).click()
        amazon_peso=self.dataToLoad['Peso en Kg del envio']
        if amazon_peso=='No Especifica':
            amazon_peso="0.1"
        self.page.locator(pshopy.cajaPesoDelProducto.selector).fill(amazon_peso)

    def get_about_this_item_str(self,number_paragraphs:int):
        if "Acerca del producto" in self.dataToLoad.keys():
            about_this_item_str=dictManipulator.dict_to_bp_w_paragraphs(self.dataToLoad["Acerca del producto"],number_paragraphs)
            return about_this_item_str
        else:
            return self.dataToLoad["Resumen de 2 a 3 parrafos separados por viñetas"]

    def save_edition(self):
        saves=self.page.query_selector_all("//span[text()='Guardar']")
        saves[len(saves)-1].click()
        self.page.wait_for_selector("span[class*='Polaris-Banner--textSuccessOnBgFill']+h2",timeout=8000)
    def go_to_custom_fields(self):
        baseUrl="https://admin.shopify.com/store/unaluka/apps/arena-custom-fields/products_editor/"
        currentUrl=self.page.url
        number=re.findall(r"\d+",currentUrl)[0]
        editUrl=baseUrl+number
        postUrl="https://app.advancedcustomfield.com/admin/load-metafield-template"
        with self.page.expect_response(postUrl,timeout=20000) as response_info:
            self.page.goto(editUrl)
        response = response_info.value
        if response.ok:
            pass
        else:
            self.status="ERROR AL CARGAR,NO SE PUDO CARGAR LA PAGINA DE LOS CUSTOM FIELDS"
            raise Exception("Error al cargar la pagina de custom fields")
        print("cargando custom fields")
    def load_custom_fields(self):
        self.page.frame_locator("iframe[name=\"app-iframe\"]").get_by_label("Disponibilidad").select_option(str(self.sheetProductData['FORMA DE VENTA']))
        webelement=self.page.locator("iframe[title='ACF: Metafields Custom Fields']")
        frame_locator=webelement.content_frame
        frame_locator.locator("div[class='fr-element fr-view']").click()
        two_systems_acf_description=self.get_about_this_item_str(4)
        frame_locator.locator("div[class='fr-element fr-view']").fill(two_systems_acf_description)
        saveUrl="https://app.advancedcustomfield.com/admin/save-metafield-template"
        with self.page.expect_response(saveUrl,timeout=30000) as response_info:
            try:
                self.page.locator("//button/span[text()='Save']").all()[0].click(timeout=8000)
            except:
                frame_locator.locator("div[class='fr-element fr-view']").press("ArrowDown")
                frame_locator.locator("div[class='fr-element fr-view']").press("Enter")
                self.page.locator("//button/span[text()='Save']").all()[0].click(timeout=5000)
        response = response_info.value
        if response.ok:
            pass
        else:
            self.status="ERROR AL CARGAR,NO SE PUDO CARGAR LA PAGINA DE LOS CUSTOM FIELDS"
            raise Exception("Error al cargar la pagina de custom fields")
        baseUrl="https://admin.shopify.com/store/unaluka/products/"
        currentUrl=self.page.url
        codeProduct=re.findall(r"\d+",currentUrl)[0]
        print(f"producto {self.dataToLoad['sku']} subido a shopify")
        self.finalUrlCreatedProduct=baseUrl+codeProduct
    def load_sub_main_shopify(self):
        self.load_title()
        self.load_descriptions()
        self.load_images() 
        self.load_prices()       
        self.load_peso()
        self.load_sku()
        self.load_stock()
        self.page.locator("select[name='status']").select_option(self.configDataSheet['MODO PUBLICACION SHOPIFY'])
        self.load_shopify_category_suggestion()
        self.load_provider()
        self.select_shopify_collections()
        self.save_edition()
        self.go_to_custom_fields()
        self.load_custom_fields()
        return self.finalUrlCreatedProduct

    def handle_login_shopify(self):
        if len(self.page.query_selector_all("h1[class='ui-heading']"))>0:
            if self.page.query_selector_all("h1[class='ui-heading']")[0].inner_text()=="Selecciona una cuenta":
                self.page.locator("div[class='user-card ']").click()
            else:
                self.page.locator("input[id='account_email']").fill("picking@unaluka.com")
                self.page.locator("span[class='ui-button__text']").click()
                self.page.locator("input[id='account_password']").fill("A123456789")
                self.page.locator("span[class='ui-button__text']").click()
                print("cuenta seleccionada")
def test_main_shopify(dataSheet=None):
    if dataSheet==None:
        with open("dataToDownLoadAndLoad.json","r",encoding="utf-8") as json_file:
            dataSheet=json.load(json_file)
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context=browser.new_context(storage_state="DropShippingAuto/src/sessions/state_shopify.json")
    loaderShopify=LoaderShopify(dataSheet['dataToLoadSheet'],
                                dataSheet['configDataSheet'],
                                context.pages[0],context,p)
    page_shopi=context.new_page()
    #context.pages[0].close()
    newProductLink="https://admin.shopify.com/store/unaluka/products/new"
    newProductLink2="https://admin.shopify.com/store/395520/products/new"
    page_shopi.goto(newProductLink)
    page_shopi.wait_for_load_state("load")
    loaderShopify.handle_login_shopify(page_shopi)
    dataToLoad=dataSheet['dataToLoadSheet']
    configData=dataSheet['configDataSheet']
    if dataToLoad:
        products=[item['sku'].strip() for item in dataToLoad]
    responseLoad=[]

    for productData in dataToLoad:
        data={
            "loadDataSheet":productData,
            "configDataSheet":configData
        }
        r=loaderShopify.load_main_sku_shopify(page_shopi,data)
        page_shopi.goto(newProductLink)
    context.storage_state(path="DropShippingAuto/src/sessions/state_shopify.json")
    context.close()
    browser.close()
    p.stop()
    #save the response in json file
    with open("DropShippingAuto/Responsedata_load.json","w",encoding="utf-8") as json_file:
        json.dump(responseLoad,json_file,indent=4,ensure_ascii=False)
    return responseLoad
if __name__ == "__main__":
    test_main_shopify()