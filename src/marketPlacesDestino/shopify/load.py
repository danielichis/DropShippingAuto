
from playwright.sync_api import sync_playwright
import time
from src.marketPlacesDestino.shopify.interfaces import productosShopify as pshopy
from src.marketPlacesDestino.shopify.interfaces import acfMetafields as acm
from src.utils.manageProducts import load_products
from src.utils.managePaths import mp
from src.utils.manipulateDicts import dc
import os

def load_descriptions(page_shopi,descs):
    diccionario=str(descs)
    codigo_js="var box=document.querySelector('iframe[id=product-description_ifr]').contentDocument.querySelector('body');var lista=document.createElement('ul');var listaDeObjetos = %s;for (const objeto of listaDeObjetos){var pelem=document.createElement('li');var stronge=document.createElement('strong');var valor=document.createTextNode(objeto.valor);stronge.textContent=objeto.campo;pelem.appendChild(stronge);pelem.appendChild(valor);lista.appendChild(pelem)};box.appendChild(lista);" %(diccionario)
    page_shopi.evaluate(codigo_js)
def load_sku(page_shopi,amazonDatSku,productDataSht,configData):
    descs=dc.dict_to_string(amazonDatSku['Detalles Tecnicos'])
    if descs=="":
        descs=dc.dict_to_string(amazonDatSku['Vista General'])

    page_shopi.wait_for_selector(pshopy.cajaNombreProducto.selector)
    #cambiar a un iframe
    page_shopi.query_selector(pshopy.cajaNombreProducto.selector).fill(amazonDatSku["titulo"])
    #page_shopi.frame_locator(pshopy.frameDescripcionProducto.selector).locator(pshopy.cajaDescripcionProducto.selector).fill(descs)
    load_descriptions(page_shopi,descs)
    page_shopi.wait_for_selector("span>input[type='file']")
    page_shopi.locator("span>input[type='file']").set_input_files(amazonDatSku['asbPathImages'])
    page_shopi.wait_for_selector("div[class*='Polaris-DropZone__Container']>div>div:nth-child(2)>div:last-child span>span",state="attached")
    page_shopi.wait_for_selector("div[class*='Polaris-DropZone__Container']>div>div:nth-child(2)>div:last-child span>span",state="visible")
    time.sleep(4)
    page_shopi.query_selector(pshopy.cajaPrecioProducto.selector).fill(productDataSht['PrecioShopify'])
    page_shopi.query_selector(pshopy.cajaPrecioComparacion.selector).fill(productDataSht['PrecioListaShopify'])
    page_shopi.query_selector(pshopy.cajaStock.selector).fill("1")
    page_shopi.query_selector(pshopy.cajaSKU.selector).fill(amazonDatSku['sku'])
    page_shopi.query_selector(pshopy.cajaPesoDelProducto.selector).fill("0.01")
    page_shopi.get_by_label("Estado").select_option(configData['modoPublicacion'])
    try:
        page_shopi.query_selector("path[d*='M13.28']").click(timeout=3000)
    except:
        pass
    page_shopi.query_selector_all("//span[text()='Guardar']")[1].click()

    page_shopi.goto("https://admin.shopify.com/store/unaluka/apps/arena-custom-fields/products_editor")
    customFrame=page_shopi.frame_locator("iframe[title='ACF: Metafields Custom Fields']")
    time.sleep(2)
    customFrame.locator(acm.cajaBuscadorProductosActivos.selector).fill(data["titulo"].replace('"',""))
    time.sleep(2)
    try:
        customFrame.locator(acm.botonBuscarProducto.selector).click(timeout=3000)
        products=customFrame.locator(acm.listaProductoParaEditar.selector,timeout=3000)
        products.first.click(timeout=3000)
    except:
        time.sleep(2)
        customFrame.locator(acm.botonBuscarProducto.selector).click()
        products=customFrame.locator(acm.listaProductoParaEditar.selector)
        products.first.click()
    page_shopi.frame_locator("iframe[name=\"app-iframe\"]").get_by_label("Disponibilidad").select_option("STOCK")
    abaoutProduct=dc.dict_to_string(amazonDatSku['Acerca del producto'])
    customFrame.locator("div[class='fr-element fr-view']").fill(abaoutProduct)
    print(f"producto {amazonDatSku['sku']} subido a shopify")
def load_main_shopify(dataSheet=None):
    p = sync_playwright().start()
    user_dir=r"C:\Users\Daniel\AppData\Local\Google\Chrome\User Data2"
    context = p.chromium.launch_persistent_context(user_dir,headless=False)
    page_shopi=context.new_page()
    context.pages[0].close()
    newProductLink="https://admin.shopify.com/store/unaluka/products/new"
    page_shopi.goto(newProductLink)
    dataToLoad=dataSheet['dataToLoad']
    configData=dataSheet['configData']
    if dataToLoad:
        products=[item['SKU'].strip() for item in dataToLoad]
    else:
        products=load_products()
    responseLoad=[]
    for productData in dataToLoad:
        amazonDatSku=mp.data_sku(productData['SKU'].strip())
        try:
            load_sku(page_shopi,amazonDatSku,productData,configData)
            load_status="success"
        except Exception as e:
            load_status="error"
        responseLoad.append({
            "sku":productData['SKU'].strip(),
            "status":load_status
        })
        page_shopi.goto(newProductLink)
    return responseLoad
if __name__ == "__main__":
    load_main_shopify()