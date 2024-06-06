
from playwright.sync_api import sync_playwright
import time
import traceback
from DropShippingAuto.src.marketPlacesDestino.shopify.interfaces import productosShopify as pshopy
from DropShippingAuto.src.marketPlacesDestino.shopify.interfaces import acfMetafields as acm
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from DropShippingAuto.src.utilsDropSh.managePaths import mp
from DropShippingAuto.src.utilsDropSh.manipulateDicts import dc
from utils.embeddings.embeding import get_top_n_match
import json
import re
import os

class LoaderShopify:
    def __init__(self,dataToLoad,sheetProductData,configSheetData,page,context,p):
        self.dataToLoad=dataToLoad
        self.page=page
        self.context=context
        self.p=p
        self.sheetProductData=sheetProductData
        self.configDataSheet=configSheetData
    def load_descriptions(self):
        descs=self.dataToLoad['descripciones']
        if type(descs)!=dict:
            raise Exception("el parametro descs debe ser un diccionario")
        listaObjetos=[]
        for k,v in descs.items():
            listaObjetos.append({
                "campo":k.replace("'","").replace('"',""),
                "valor":": "+v.replace("'","").replace('"',"")
            })
        diccionario=str(listaObjetos)
        codigo_js="var box=document.querySelector('iframe[id=product-description_ifr]').contentDocument.querySelector('body');var lista=document.createElement('ul');var listaDeObjetos = %s;for (const objeto of listaDeObjetos){var pelem=document.createElement('li');var stronge=document.createElement('strong');var valor=document.createTextNode(objeto.valor);stronge.textContent=objeto.campo;pelem.appendChild(stronge);pelem.appendChild(valor);lista.appendChild(pelem)};box.appendChild(lista);" %(diccionario)
        self.page.evaluate(codigo_js)

    def load_shopify_category_suggestion(self):
        try:
            self.page.query_selector("path[d*='M13.28']").click(timeout=3000)
        except:
            pass

    def select_shopify_collections(self):
        amazonDatSku=self.dataToLoad
        self.page.get_by_role("combobox", name="Proveedor").fill("unaluka")
        self.page.locator("input[id='CollectionsAutocompleteField1']").click()
        currentCollections=self.page.locator("ul[aria-labelledby='CollectionsAutocompleteField1Label'] li span div").all_inner_texts()
        TopCollections=get_top_n_match(amazonDatSku,currentCollections,3)
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
            url=self.load_sku()
            tb="ok"
        except Exception as e:
            tb=traceback.format_exc()
            url=""
            self.status="ERROR AL CARGAR"
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
        list_providers=self.page.locator("ul[role='listbox'] li").all_inner_texts()

    def load_sku(self):

        if self.dataToLoad['Detalles Tecnicos']!={}:
            descs=self.dataToLoad['Detalles Tecnicos']
        elif self.dataToLoad['Vista General']!={}:
            descs=self.dataToLoad['Vista General']
        elif self.dataToLoad['Acerca del producto']!={}:
            descs=self.dataToLoad['Acerca del producto']
        elif self.dataToLoad['descripciones']!={}:
            descs=self.dataToLoad['descripciones']
        else:
            raise Exception("no se encontro una descripcion para el producto")
        self.page.wait_for_selector(pshopy.cajaNombreProducto.selector)
        #cambiar a un iframe
        self.page.query_selector(pshopy.cajaNombreProducto.selector).fill(self.dataToLoad["titulo"])
        self.load_descriptions()
        self.page.frame_locator(pshopy.frameDescripcionProducto.selector).locator(pshopy.cajaDescripcionProducto.selector).click()
        self.page.wait_for_selector("span>input[type='file']")
        self.page.locator("span>input[type='file']").set_input_files(self.dataToLoad['imagesPath'])
        self.page.wait_for_selector(pshopy.cajaPrecioProducto.selector)
        self.page.locator(pshopy.cajaPrecioProducto.selector).click()
        self.page.locator(pshopy.cajaPrecioProducto.selector).fill(str(self.sheetProductData['PRECIO FINAL MARKETPLACE']),timeout=3000)
        self.page.locator(pshopy.cajaPrecioComparacion.selector).click()
        self.page.locator(pshopy.cajaPrecioComparacion.selector).fill(str(self.sheetProductData['PRECIO LISTA MARKETPLACE']),timeout=3000)
        self.page.locator(pshopy.cajaStock.selector).click()
        self.page.locator(pshopy.cajaStock.selector).fill("1")
        self.page.locator(pshopy.cajaSKU.selector).click()
        self.page.locator(pshopy.cajaSKU.selector).fill(self.dataToLoad['sku'])
        self.page.locator(pshopy.cajaPesoDelProducto.selector).click()
        self.page.locator(pshopy.cajaPesoDelProducto.selector).fill("0.01")
        self.page.get_by_label("Estado").select_option(self.configDataSheet['MODO PUBLICACION SHOPIFY'])
        self.load_shopify_category_suggestion()
        self.select_shopify_collections()
        
        self.page.query_selector_all("//span[text()='Guardar']")[1].click()
        self.page.wait_for_selector("span[class*='Polaris-Banner--textSuccessOnBgFill']+h2",timeout=8000)
        self.page.goto("https://admin.shopify.com/store/unaluka/apps/arena-custom-fields/products_editor")
        customFrame=self.page.frame_locator("iframe[title='ACF: Metafields Custom Fields']")
        customFrame.locator(acm.cajaBuscadorProductosActivos.selector).fill(self.dataToLoad["titulo"].replace('"',""))
        time.sleep(3)
        try:
            customFrame.locator(acm.botonBuscarProducto.selector).click(timeout=3000)
            products=customFrame.locator(acm.listaProductoParaEditar.selector)
            products.first.click(timeout=3000)
        except:
            time.sleep(2)
            customFrame.locator(acm.botonBuscarProducto.selector).click(timeout=3000)
            products=customFrame.locator(acm.listaProductoParaEditar.selector)
            products.first.click(timeout=3000)
        self.page.frame_locator("iframe[name=\"app-iframe\"]").get_by_label("Disponibilidad").select_option("STOCK")
        abaoutProduct=dc.dict_to_string(self.dataToLoad['Acerca del producto'])

        customFrame.locator("div[class='fr-element fr-view']").fill(abaoutProduct)
        baseUrl="https://admin.shopify.com/store/unaluka/products/"
        currentUrl=self.page.url
        codeProduct=re.findall(r"\d+",currentUrl)[0]
        print(f"producto {self.dataToLoad['sku']} subido a shopify")
        self.status="CARGADO CORRECTAMENTE"
        return baseUrl+codeProduct

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
        with open("DropShippingAuto/dataToLoad.json","r",encoding="utf-8") as json_file:
            dataSheet=json.load(json_file)
    p = sync_playwright().start()
    user_dir=mp.profiel_path
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