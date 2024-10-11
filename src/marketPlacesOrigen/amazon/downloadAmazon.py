import time
from playwright.sync_api import sync_playwright,expect
import json
import requests
import io
from tqdm import tqdm
import os
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from utils.dinamicMassivArgsExtractions import generate_dinamic_title_per_mkp,dinamic_two_systems_description_dict
from DropShippingAuto.src.utilsDropSh.magic_fields import get_static_fields_with_openai
from PIL import Image
from DropShippingAuto.src.utilsDropSh.imageConverters import resize_image
from utils.managePaths import mp
from utils.manipulateDicts import dictManipulator
from utils.imgHandling.imgHandling import resize_original_images_per_mkp
from utils.structures import get_element_with_more_fields
import traceback
import csv
from utils.manipulateDicts import dictManipulator
import shutil

def get_overView(pw_page):
    overViewSelectors=["div[id='productOverview_feature_div'] div[class='a-section a-spacing-small a-spacing-top-small'] tr","div[id='productOverview_feature_div'] div[class='a-section a-spacing-small a-spacing-top-small'] tr"]
    try:
        pw_page.wait_for_selector("div[id='productOverview_feature_div'] div[class='a-section a-spacing-small a-spacing-top-small'] tr",timeout=3000)
    except:
        pass
    overView=pw_page.query_selector_all("div[id='productOverview_feature_div'] div[class='a-section a-spacing-small a-spacing-top-small'] tr")


    overVies={}
    for view in overView:
        try:
            overVies[view.query_selector("td:nth-child(1) span").inner_text()]=view.query_selector("td:nth-child(2) span").inner_text().replace("\u200e","")
        except:
            pass

    if len(overView)==0:
        overView=pw_page.query_selector_all("div[id='feature-bullets'] li")
        for i,view in enumerate(overView):
            try:
                overVies[view.query_selector("span").inner_text().replace("\u200e","").split(":")[0]]=':'.join(view.query_selector("span").inner_text().replace("\u200e","").split(":")[1:])
            except:
                pass
    if len(overView)==0:
        overView=pw_page.query_selector_all("div:has(>h3[class='product-facts-title'])>div>div")
        for view in overView:
            try:
                overVies[view.query_selector("div:nth-child(1)").inner_text().replace("\u200e","")]=view.query_selector("div:nth-child(2)").inner_text().replace("\u200e","")
            except:
                pass
    return overVies


def scroll_to_bottom_slowly(pw_page, timeout_ms=20000):  # timeout_ms is the maximum allowed time in milliseconds
    pw_page.evaluate(f"""
        async () => {{
            const startTime = new Date().getTime();  // Initialize start time
            const timeout = {timeout_ms};  // Timeout in milliseconds
            const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
            while (window.scrollY + window.innerHeight < document.body.scrollHeight) {{
                window.scrollBy(0, 250);  // Corrected comment: Scroll down by 250 pixels
                await delay(50);  // Corrected comment: Wait for 50 milliseconds
                const elapsedTime = new Date().getTime() - startTime;
                if (elapsedTime > timeout) {{  // Check if timeout is exceeded
                    break;  // Stop scrolling if timeout is exceeded
                }}
            }}
        }}
    """)

def get_field_from_search_bar(pw_page,field):
    #url https://www.amazon.com/ask/livesearch/detailPageSearch/search?query=peso&asin=B0815XFSGK&forumId=&liveSearchSessionId=c196fd3e-3b30-41c6-b949-216cd5287a70&liveSearchPageLoadId=b4aedb69-c00e-4229-bebe-6dd7a5205bda&searchSource=LIVE_SEARCH_SOURCE&askLanguage=es_US&isFromSecondaryPage=
    #scroll to the search bar
    try:
        scroll_to_bottom_slowly(pw_page)
        #pw_page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        input_searcher=pw_page.locator("input[type='search']")
        expect(input_searcher).to_be_visible()
        input_searcher.scroll_into_view_if_needed()
        input_searcher.fill(field,timeout=5000)
        field_locator=pw_page.locator("div[class='a-section askBtfSearchResultsViewableContent'] span:has(span[class='matches'])").first
        expect(field_locator).to_be_visible(timeout=8000)
        fields=field_locator.inner_text()
    except Exception as e:
        print(str(e))
        fields="No Especifica"
    return  fields

def get_technicalDetails(pw_page):
    if len(pw_page.query_selector_all("table[id*='productDetails_techSpec_section'] tr"))>0:
        technicalDetails=pw_page.query_selector_all("table[id*='productDetails_techSpec_section'] tr")
        child="th"
    elif len(pw_page.query_selector_all("div[id=poExpander] tbody tr"))>0:
        technicalDetails=pw_page.query_selector_all("div[id=poExpander] tbody tr")
        child="td"
    elif len(pw_page.query_selector_all("table[id*='technicalSpecifications'] tr"))>0:
        technicalDetails=pw_page.query_selector_all("table[id*='technicalSpecifications'] tr")
        child="th"
    elif len(pw_page.query_selector_all("table[class='a-bordered'] tr"))>0:
        technicalDetails=pw_page.query_selector_all("table[class='a-bordered'] tr")
        child="td"
    else:
        technicalDetails=[]

    technicalDetailsDict={}
    for technicalDetail in technicalDetails:
        technicalDetailsDict[technicalDetail.query_selector(f"{child}:nth-child(1)").inner_text()]=technicalDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
    return technicalDetailsDict

def get_aboutProduct(pw_page):
    
    selectorsOptions=["div#feature-bullets li span","div[id='productFactsDesktop_feature_div'] ul li>span"]
    aboutProductDict={}
    if len(pw_page.query_selector_all(selectorsOptions[0]))>0:
        aboutProduct=pw_page.query_selector_all(selectorsOptions[0])
    elif len(pw_page.query_selector_all(selectorsOptions[1]))>0:
        aboutProduct=pw_page.query_selector_all(selectorsOptions[1])
    else:
        return None
    for i,aboutP in enumerate(aboutProduct):
        try:
            aboutProductDict[dictManipulator.fisrt_substring_before_double_dot(aboutP.inner_text())]=dictManipulator.all_substring_affer_double_dot(aboutP.inner_text())
        except:
            aboutProductDict[str(i)+".-"]=aboutP.inner_text()
    
    # if aboutProductDict==None:
    #     aboutProductDict=""

    return aboutProductDict

def get_otherDetails(pw_page):
    otherDetails=pw_page.query_selector_all("table[class*='_product-comparison'] tr")
    otherDetailsDict={}
    for otherDetail in otherDetails:
        otherDetailsDict[otherDetail.query_selector("td:nth-child(1)").inner_text()]=otherDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
    return otherDetailsDict

def get_aditionalInfo(pw_page):
    aditionalInfo=pw_page.query_selector_all("div#productDetails_db_sections tr")
    aditionalInfoDict={}
    for aditionalInfo in aditionalInfo:
        aditionalInfoDict={}
        aditionalInfoDict[aditionalInfo.query_selector("th:nth-child(1)").inner_text()]=aditionalInfo.query_selector("td:nth-child(2)").inner_text()

    return aditionalInfoDict
def get_bulletDetails(pw_page):
    bulletInfo=pw_page.query_selector_all("div#detailBullets_feature_div li")
    bulletInfoDict={}
    for bullet in bulletInfo:
        try:
            bulletInfoDict[bullet.query_selector("span span").inner_text().replace("\u200e","").replace("\u200f","")]=bullet.query_selector("span:nth-child(2)").inner_text().replace("\u200e","")
        except:
            pass
    return bulletInfoDict

def get_urls(pw_page):
    minipics=pw_page.query_selector_all("li[data-csa-c-action=image-block-alt-image-hover]")
    for mini in minipics:
        mini.hover()
        time.sleep(0.2)
    urls=pw_page.query_selector_all("img[data-old-hires]")
    urlsList=[]
    for url in urls:
        urlsList.append(url.get_attribute("data-old-hires"))
    print(urlsList)
    #testing case for when images dont appear
    #urlsList=[]


    # <img alt="Microsoft Tablet Surface Go 4 - Full HD de 10,5&amp;#34; - 8 GB - 64 GB de almacenamiento - Platino" src="https://m.media-amazon.com/images/I/51z-H1CywML._AC_SX425_.jpg" data-old-hires="" onload="markFeatureRenderForImageBlock(); 
    # if(this.width/this.height > 1.0){this.className += ' a-stretch-horizontal'}else{this.className += ' a-stretch-vertical'};this.onload='';setCSMReq('af');if(typeof addlongPoleTag === 'function'){ addlongPoleTag('af','desktop-image-atf-marker');};setCSMReq('cf')" data-a-image-name="landingImage" class="a-dynamic-image a-stretch-horizontal" id="landingImage" 
    # data-a-dynamic-image="{&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SX569_.jpg&quot;:[569,569],&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SX425_.jpg&quot;:[425,425],&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SX466_.jpg&quot;:[466,466],&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SX679_.jpg&quot;:[679,679],&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SY355_.jpg&quot;:[355,355],&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SX522_.jpg&quot;:[522,522],&quot;https://m.media-amazon.com/images/I/51z-H1CywML._AC_SY450_.jpg&quot;:[450,450]}" style="max-width: 380px; max-height: 274.867px;">

    if len(urlsList)>0:
        if len(urlsList)==1 and urlsList[0]=="":
            return None
            #pass
            #raise Exception("No se encontraron URLs para las imágenes")
        else:
            return urlsList
    else:
        return None
        #pass
        #raise Exception("No se encontraron URLs para las imágenes")

def get_importantInfo(pw_page):
    importantInfo=pw_page.query_selector_all("div#important-information div.a-section:not(:has(a))")
    importantInfoList=[]
    for info in importantInfo:
        try:
            importantInfoList.append({
                info.query_selector("h4").inner_text():info.query_selector("p:nth-child(3)").inner_text()
            })
        except:
            pass
    return importantInfoList

def img_down(links,skuFolder):
    skuImageFolder=os.path.join(skuFolder,"images","originals")
    os.makedirs(skuFolder,exist_ok=True)
    os.makedirs(skuImageFolder,exist_ok=True)
    if links!=None:
        print("Se encontraron links de imágenes para descargar")
        for link in links:
            if link!="":
                response  = requests.get(link).content 
                image_file = io.BytesIO(response)
                image  = Image.open(image_file)   
                sku=link.split('/')[-1]
                imagePath=os.path.join(skuImageFolder,sku)
                with open(imagePath , "wb") as f:
                    image.save(f , "JPEG")
    else:
        print("No se encontraron links de imágenes para descargar")
        print("Colocando imagen por defecto")
        shutil.copy(mp.defaultNoImgPath,skuImageFolder)
    
    resize_original_images_per_mkp(skuFolder)


                
def get_comparitions(pw_page):
    rows=pw_page.query_selector_all("table[id='HLCXComparisonTable'] tr[class='comparison_other_attribute_row']")
    comparisonDict={}
    for row in rows:
        comparisonDict[row.query_selector("th span").inner_text()]=row.query_selector("td:nth-child(2) span").inner_text()
    return comparisonDict
def get_descriptions(pw_page):
    descriptions=pw_page.query_selector("div#productDescription span")
    dicDescs={}
    if descriptions:
        list_Descs=descriptions.inner_text().split("\n\n")
        if len(list_Descs)==1:
            list_Descs=[x+"." for x in descriptions.inner_text().split(".") if x!=""]
            for i,desc in enumerate(list_Descs):
                dicDescs[str("-")]=desc
        elif len(list_Descs)>1:
            for i,desc in enumerate(list_Descs):
                #print("texto en linea: "+desc)
                try:
                    d1=desc.split(":")[0]
                    d2=desc.split(":")[1]
                    dicDescs[d1]=d2
                except: 
                    pass
        else:
            pass
    return dicDescs
def get_classificaction(pw_page):
    try:
        pw_page.wait_for_selector("div#wayfinding-breadcrumbs_feature_div li span[class=a-list-item]",timeout=3000)
        classificaction=pw_page.locator("div#wayfinding-breadcrumbs_feature_div li span[class=a-list-item]").all_inner_texts()
    except:
        classificaction="sin clasificacion"
    return classificaction

def get_price(pw_page):
    try:
        price=pw_page.query_selector("div[id='corePrice_feature_div'] span[class='a-offscreen']").inner_text()
    except:
        price="no especifico"
    return price

def get_title(pw_page):
    full_text=pw_page.locator("body").inner_text()
    if full_text.find("¿Estás buscando algo?\nLo sentimos.")!=-1:
        raise Exception("ERROR, NO EXISTE PRODUCTO O INTERNET LENTO")
    title=pw_page.query_selector("span[id='productTitle']").inner_text()
    return title

def get_note(pw_page):
    try:
        note=pw_page.query_selector("div#universal-product-alert span:nth-child(2)").inner_text()
    except:
        note=None
def get_garanty(pw_page):
    try:
        garanty=pw_page.query_selector("h1.a-size-medium.a-spacing-small.secHeader+div>span:nth-child(3)").inner_text()
    except:
        garanty=None
    return garanty

def get_product_information(pw_page):
    productInformation=pw_page.query_selector_all("table[id*='productDetails_detailBullets'] tr")
    productInformationDict={}
    for info in productInformation:
        productInformationDict[info.query_selector("th").inner_text()]=info.query_selector("td").inner_text().replace("\u200e","")
    return productInformationDict

def download_sub_main_sku_amazon_product(pw_page,sku):
    try:    
        download_sku(pw_page,sku)
        status="DESCARGADO CORRECTAMENTE"
        newProduct="yes"
        tb="ok"
        status_code=200
    except Exception as e:
        tb=traceback.format_exc()
        print(tb)
        newProduct="yes"
        status="ERROR EN LA DESCARGA"
        status_code=500
        save_screenshot(pw_page,sku)
        #pw_page.close()
    return {
        "status":status,
        "newProduct":newProduct,
        "log":tb,
        "status_code":status_code
    }
def get_sku_amazon_product(pw_page,product):
    sku=product['SKU'].strip()
    skuFolder=os.path.join(mp.sku_folder_path,sku)
    skuFolderImages=os.path.join(skuFolder,"images")
    skuFolderData=os.path.join(skuFolder,"data.json")
    defaulResponse={
        "product":sku,
        "status":"",
        "url":f"https://www.amazon.com/dp/{sku}",
        "marketplace":"amazon",
        "condition":"",
        "log":"",
        "fecha":time.strftime("%Y-%m-%d %H:%M:%S")
    }
    if not os.path.exists(skuFolder):
        #download_sku(pw_page,sku,urlProducto,skuFolder)
        r=download_sub_main_sku_amazon_product(pw_page,sku)
        status=r['status']
        newProduct=r['newProduct']
        tb=r['log']
        status_code=r['status_code']
    elif  not os.path.exists(skuFolderImages) or not os.path.exists(skuFolderData):
        r=download_sub_main_sku_amazon_product(pw_page,sku)
        status=r['status']
        newProduct=r['newProduct']
        tb=r['log']
        status_code=r['status_code']

    else:
        status="DESCARGADO CORRECTAMENTE"
        newProduct="no"
        tb="ok"
        status_code=200

    defaulResponse['status']=status
    defaulResponse['condition']=newProduct
    defaulResponse['log']=tb
    defaulResponse['fecha']=time.strftime("%Y-%m-%d %H:%M:%S")
    defaulResponse['status_code']=status_code
    return defaulResponse
def download_sku(pw_page,sku):
    urlProducto=f"https://www.amazon.com/dp/{sku}"
    skuFolder=os.path.join(mp.sku_folder_path,sku)
    pw_page.goto(urlProducto)
    urls_images=get_urls(pw_page)
    print("\nPagina cargada en el producto "+sku)
    classificaction=get_classificaction(pw_page)
    try:
        title=get_title(pw_page)
    except:
        raise Exception("ERROR, NO EXISTE PRODUCTO O INTERNET LENTO")
    price=get_price(pw_page)
    overView=get_overView(pw_page)
    note=get_note(pw_page)
    technicalDetails=get_technicalDetails(pw_page)
    aboutProduct=get_aboutProduct(pw_page)
    otherDetails=get_otherDetails(pw_page)
    aditionalInfo=get_aditionalInfo(pw_page)
    bulletDetails=get_bulletDetails(pw_page)
    importantInfo=get_importantInfo(pw_page)
    comparitions=get_comparitions(pw_page)
    descriptions=get_descriptions(pw_page)
    productInformation=get_product_information(pw_page)
    #garanty=get_garanty(pw_page)    
    img_down(urls_images,skuFolder)
    weight_description=get_field_from_search_bar(pw_page,"peso")
    
    data={
        "sku":sku,
        "url":urlProducto,
        "clasificacion":classificaction,
        "titulo":title,
        "precio":price,
        "descripciones":descriptions,
        "Vista General":overView,
        "Detalles Tecnicos":technicalDetails,
        "Acerca del producto":aboutProduct,
        "Otros detalles":otherDetails,
        "Contenido de la caja":bulletDetails,
        "Mas detalles Tecnicos":comparitions,
        "Informacion Importante":importantInfo,
        "Informacion Adicional":aditionalInfo,
        "informacion del producto":productInformation,
        "Nota":note,
        #"Links Imagenes":urls_images,
        "Peso en Kg del envio":weight_description
    }

    ##Erasing any key-value pair that contains any of the word in the list
    pairs_to_remove=["garantia","garantía","Producto en amazon.com desde","ASIN","precio","Forma del articulo","Clasificación en los más vendidos de Amazon","Opinión media de los clientes"]
    pairs_to_remove_otrosdetalles=["Peso Ligero","Vendido por","Pantalla táctil","Excelente inversión","Calidad de pantalla","Vida útil de la batería","Para juegos","Calificaciones de los clientes","precio"]
    dictManipulator.remove_pair_holding_word_from_dict(data,pairs_to_remove)
    ## Borrando peso ligero del subdiccionario otros detalles
    if "Peso Ligero" in data["Otros detalles"].keys():
        print("Borrando peso ligero del diccionario")
        del data["Otros detalles"]["Peso Ligero"]

    ####
    print("Extrayendo campos adicionales con OpenAI...")
    more_fields=get_static_fields_with_openai(data)
    data.update(more_fields)

    if data['Peso en Kg del envio'].upper()=="NO ESPECIFICA":
        data['Peso en Kg del envio']=data['Peso en Kg del producto']

    print("Generando títulos según lineamientos...")
    marketplaces_list=["SHOPIFY","RIPLEY","REAL PLAZA"]
    titles_first_options=[data["Titulo,corregido si está mal redactado, en un máximo de 150 caracteres con unidades convertidas de ser necesario"],
                          data["Titulo,corregido si está mal redactado, entre 110 y 120 caracteres con unidades convertidas de ser necesario"],
                          data["Titulo,corregido si está mal redactado, entre 80 y 90 caracteres con unidades convertidas de ser necesario"]
                          ]
    
    data["titulos_generados"]={}

    for i,mkp in enumerate(marketplaces_list):
        generated_title=generate_dinamic_title_per_mkp(str(data),mkp)
        if generated_title.upper()=="NO ENCONTRADO":
            generated_title=titles_first_options[i]
        print(f"Titulo generado para {mkp}: {generated_title}")
        data["titulos_generados"][mkp.lower()]=generated_title

    #data["titulos_generados"]={
    #    "shopify":title_shopify,
    #    "ripley":title_ripley,
    #    "realplaza":title_realplaza
    #}
    print(data["titulos_generados"])

    print("Escogiendo sub-diccionario de mayor tamaño...")
    list_descripciones=[data["descripciones"],data["Vista General"],data["Detalles Tecnicos"],
                        data["informacion del producto"],data["Contenido de la caja"],
                        data["Mas detalles Tecnicos"]]
    if data["informacion del producto"]!={}:
        description_dict=data["informacion del producto"]
    else:
        description_dict=get_element_with_more_fields(list_descripciones)

    if description_dict=={} or description_dict==None:
        raise Exception("No se encontraron descripciones,información insuficiente 1")


    new_description=dictManipulator.extract_largest_dict_string(dinamic_two_systems_description_dict(description_dict))
    if new_description=={} or new_description==None:
        print("No se pude reconvertir el diccionario,devolviendo diccionario original")
        data["descripciones"]=description_dict
    else:
        data["descripciones"]=new_description
    
    if "Acerca del producto" in data.keys():
        new_aboutProduct=dictManipulator.extract_largest_dict_string(dinamic_two_systems_description_dict(data["Acerca del producto"]))
        if new_aboutProduct!={} and new_aboutProduct!=None:
            data["Acerca del producto"]=new_aboutProduct 
    else:
        print("El campo 'Acerca del producto' se borró porque no se encontró información")

    if description_dict=={} or description_dict==None:
        raise Exception("No se encontraron descripciones,información insuficiente 2")

    print("Guardando información en archivo json...")
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def remove_all_sku_folder():
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    skuFolder=os.path.join(currentFolder,"skus_Amazon")
    for sku in os.listdir(skuFolder):
        skuPath=os.path.join(skuFolder,sku)
        os.remove(skuPath)
def save_screenshot(pw_page,sku):
    skuFolder=os.path.join(mp.sku_folder_path,sku)
    if not os.path.exists(skuFolder):
        os.makedirs(skuFolder)
    picPath=os.path.join(skuFolder,"screenshot.png")
    #pw_page.screenshot(path=picPath)

def download_info(dataSheet=None):
    if dataSheet:
        products=[item for item in dataSheet]
    else:
        products=get_data_to_download()
        products=[x for x in products['dataToLoad']]
    p = sync_playwright().start()
    user_dir=mp.get_current_chrome_profile_path()
    context = p.chromium.launch_persistent_context(user_dir,headless=False)
    pw_page = context.new_page()
    downloadsResponse=[]
    for product in tqdm(products):
        r=get_sku_amazon_product(pw_page,product)
        downloadsResponse.append({
            "sku":product['SKU'],
            "status":r['status'],
            "newProduct":r['condition'],
            "product":r['product']
        })
    context.storage_state(path="DropShippingAuto/src/sessions/state_amazon.json")
    context.close()
    p.stop()
    return downloadsResponse
if __name__ == "__main__":
    download_info()