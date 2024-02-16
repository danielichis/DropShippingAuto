
from playwright.sync_api import sync_playwright
import time
from src.marketPlacesDestino.shopify.interfaces import productosShopify as pshopy
from src.marketPlacesDestino.shopify.interfaces import acfMetafields as acm
from src.utils.manageProducts import load_products
from src.utils.managePaths import mp
from src.utils.manipulateDicts import dc
from src.utils.embeddings.embeding import get_top_n_match
import re
import os

def load_descriptions(page_shopi,descs):
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
    page_shopi.evaluate(codigo_js)

def load_shopify_category_suggestion(page_shopi):
    try:
        page_shopi.query_selector("path[d*='M13.28']").click(timeout=3000)
    except:
        pass

def select_shopify_collections(page_shopi,amazonDatSku):
    page_shopi.get_by_role("combobox", name="Proveedor").fill("unaluka")
    page_shopi.locator("input[id='CollectionsAutocompleteField1']").click()
    currentCollections=page_shopi.locator("ul[aria-labelledby='CollectionsAutocompleteField1Label'] li span div").all_inner_texts()
    TopCollections=get_top_n_match(amazonDatSku,currentCollections,3)
    #page_shopi.select_option("Colecciones",name="Colecciones")
    #page_shopi.locator("div:has(>ul[aria-labelledby='CollectionsAutocompleteField1Label'])").scroll_into_view_if_needed()    
    for collection in TopCollections:
        #page_shopi.get_by_role("combobox", name="Colecciones").fill()
        page_shopi.get_by_role("option", name=collection['collecion'],exact=True).locator("div").nth(1).click()
        #page_shopi.locator(f"//span/div[text()={collection['collecion']}]").click()
        #page_shopi.get_by_role("combobox", name="Colecciones").fill("")

def load_sku(page_shopi,amazonDatSku,productDataSht,configData):
    if amazonDatSku['Detalles Tecnicos']!={}:
        descs=amazonDatSku['Detalles Tecnicos']
    elif amazonDatSku['Vista General']!={}:
        descs=amazonDatSku['Vista General']
    elif amazonDatSku['Acerca del producto']!={}:
        descs=amazonDatSku['Acerca del producto']
    elif amazonDatSku['descripciones']!={}:
        descs=amazonDatSku['descripciones']
    else:
        raise Exception("no se encontro una descripcion para el producto")
    page_shopi.wait_for_selector(pshopy.cajaNombreProducto.selector)
    #cambiar a un iframe
    page_shopi.query_selector(pshopy.cajaNombreProducto.selector).fill(amazonDatSku["titulo"])
    load_descriptions(page_shopi,descs)
    page_shopi.frame_locator(pshopy.frameDescripcionProducto.selector).locator(pshopy.cajaDescripcionProducto.selector).click()
    page_shopi.wait_for_selector("span>input[type='file']")
    page_shopi.locator("span>input[type='file']").set_input_files(amazonDatSku['asbPathImages'])
    page_shopi.wait_for_selector(pshopy.cajaPrecioProducto.selector)
    page_shopi.locator(pshopy.cajaPrecioProducto.selector).click()
    page_shopi.locator(pshopy.cajaPrecioProducto.selector).fill(productDataSht['PrecioShopify'],timeout=3000)
    page_shopi.locator(pshopy.cajaPrecioComparacion.selector).click()
    page_shopi.locator(pshopy.cajaPrecioComparacion.selector).fill(productDataSht['PrecioListaShopify'],timeout=3000)
    page_shopi.locator(pshopy.cajaStock.selector).click()
    page_shopi.locator(pshopy.cajaStock.selector).fill("1")
    page_shopi.locator(pshopy.cajaSKU.selector).click()
    page_shopi.locator(pshopy.cajaSKU.selector).fill(amazonDatSku['sku'])
    page_shopi.locator(pshopy.cajaPesoDelProducto.selector).click()
    page_shopi.locator(pshopy.cajaPesoDelProducto.selector).fill("0.01")
    page_shopi.get_by_label("Estado").select_option(configData['modoPublicacion'])
    load_shopify_category_suggestion(page_shopi)
    select_shopify_collections(page_shopi,amazonDatSku)
    page_shopi.query_selector_all("//span[text()='Guardar']")[1].click()
    page_shopi.wait_for_selector("span[class*='Polaris-Banner--textSuccessOnBgFill']+h2",timeout=4000)
    page_shopi.goto("https://admin.shopify.com/store/unaluka/apps/arena-custom-fields/products_editor")
    customFrame=page_shopi.frame_locator("iframe[title='ACF: Metafields Custom Fields']")
    customFrame.locator(acm.cajaBuscadorProductosActivos.selector).fill(amazonDatSku["titulo"].replace('"',""))
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
    page_shopi.frame_locator("iframe[name=\"app-iframe\"]").get_by_label("Disponibilidad").select_option("STOCK")
    abaoutProduct=dc.dict_to_string(amazonDatSku['Acerca del producto'])
    customFrame.locator("div[class='fr-element fr-view']").fill(abaoutProduct)
    baseUrl="https://admin.shopify.com/store/unaluka/products/"
    currentUrl=page_shopi.url
    codeProduct=re.findall(r"\d+",currentUrl)[0]
    print(f"producto {amazonDatSku['sku']} subido a shopify")
    return baseUrl+codeProduct

def load_main_shopify(dataSheet=None):
    p = sync_playwright().start()
    user_dir=mp.profiel_path
    browser = p.chromium.launch(headless=False)
    context=browser.new_context(storage_state="src/sessions/state_shopify.json")
    #context = p.chromium.launch_persistent_context(user_dir,headless=False)
    #context = p.chromium.launch_persistent_context(user_dir,headless=False,channel="chrome")
    #context=browser.new_context(storage_state="state.json")
    page_shopi=context.new_page()
    #context.pages[0].close()
    newProductLink="https://admin.shopify.com/store/unaluka/products/new"
    newProductLink2="https://admin.shopify.com/store/395520/products/new"
    page_shopi.goto(newProductLink)
    dataToLoad=dataSheet['dataToLoad']
    configData=dataSheet['configData']
    if dataToLoad:
        products=[item['sku'].strip() for item in dataToLoad]
    else:
        products=load_products()
    responseLoad=[]
    for productData in dataToLoad:
        try:
            amazonDatSku=mp.data_sku(productData['sku'].strip())
            url=load_sku(page_shopi,amazonDatSku,productData,configData)
            load_status="Cargado correctamente"
        except Exception as e:
            load_status="ERROR:"+str(e)
            url=""
        responseLoad.append({
            "sku":productData['sku'].strip(),
            "status_l":load_status,
            "url":url
        })
        page_shopi.goto(newProductLink)
    context.storage_state(path="src/sessions/state_shopify.json")
    context.close()
    browser.close()
    p.stop()
    return responseLoad
if __name__ == "__main__":
    load_main_shopify()