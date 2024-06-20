import time
from playwright.sync_api import sync_playwright
import json
import requests
import io
from tqdm import tqdm
import os
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from DropShippingAuto.src.utilsDropSh.magic_fields import get_static_fields_with_openai
from PIL import Image
from DropShippingAuto.src.utilsDropSh.imageConverters import resize_image
from utils.managePaths import mp
from utils.manipulateDicts import dictManipulator
import traceback
import csv

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

def get_technicalDetails(pw_page):
    technicalDetails=pw_page.query_selector_all("table#productDetails_techSpec_section_1 tr")
    
    if len(pw_page.query_selector_all("table#productDetails_techSpec_section_1 tr"))>0:
        technicalDetails=pw_page.query_selector_all("table#productDetails_techSpec_section_1 tr")
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

    technicalDetailsDict={}
    for technicalDetail in technicalDetails:
        technicalDetailsDict[technicalDetail.query_selector(f"{child}:nth-child(1)").inner_text()]=technicalDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
    return technicalDetailsDict

def get_abaoutProduct(pw_page):
    
    selectorsOptions=["div#feature-bullets li span","div[id='productFactsDesktop_feature_div'] ul li>span"]
    abaoutProductDict={}
    if len(pw_page.query_selector_all(selectorsOptions[0]))>0:
        abaoutProduct=pw_page.query_selector_all(selectorsOptions[0])
    elif len(pw_page.query_selector_all(selectorsOptions[1]))>0:
        abaoutProduct=pw_page.query_selector_all(selectorsOptions[1])
        for i,abaoutP in enumerate(abaoutProduct):
            try:
                abaoutProductDict[dictManipulator.fisrt_substring_before_double_dot(abaoutP.inner_text())]=dictManipulator.all_substring_affer_double_dot(abaoutP.inner_text())
            except:
                abaoutProductDict[str(i)+".-"]=abaoutP.inner_text()
    return abaoutProductDict

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
    urls=pw_page.query_selector_all("img[data-old-hires]")
    urlsList=[]
    for url in urls:
        urlsList.append(url.get_attribute("data-old-hires"))
    return urlsList

def get_importantInfo(pw_page):
    importantInfo=pw_page.query_selector_all("div#important-information div.a-section:not(:has(a))")
    importantInfoList=[]
    for info in importantInfo:
        importantInfoList.append({
            info.query_selector("h4").inner_text():info.query_selector("p:nth-child(3)").inner_text()
        })
    return importantInfoList
def img_down(links,skuFolder):
    skuImageFolder=os.path.join(skuFolder,"images")
    os.makedirs(skuFolder)
    os.makedirs(skuImageFolder)
    for link in links:
        if link!="":
            response  = requests.get(link).content 
            image_file = io.BytesIO(response)
            image  = Image.open(image_file)
            resized_image = image.resize((1000, 1000))
            sku=link.split('/')[-1]
            imagePath=os.path.join(skuImageFolder,sku)
            with open(imagePath , "wb") as f:
                resized_image.save(f , "JPEG")
                
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

def get_sku_amazon_product(pw_page,product):
    sku=product['SKU'].strip()
    skuFolder=os.path.join(mp.sku_folder_path,sku)
    if not os.path.exists(skuFolder):
        #download_sku(pw_page,sku,urlProducto,skuFolder)
        try:    
            download_sku(pw_page,sku)
            status="descargado correctamente"
            newProduct="yes"
            tb="ok"    
        except Exception as e:
            tb=traceback.format_exc()
            print(e)
            newProduct="yes"
            status="ERROR:"+str(e)
            save_screenshot(pw_page,skuFolder)
            pw_page.close()
    else:
        status="descargado correctamente"
        newProduct="no"
        tb="ok"
    response={
        "product":sku,
        "status":status,
        "url":f"https://www.amazon.com/dp/{sku}",
        "marketplace":"amazon",
        "condition":newProduct,
        "log":tb,
        "fecha":time.strftime("%Y-%m-%d %H:%M:%S")
    }
    return response
def download_sku(pw_page,sku):
    urlProducto=f"https://www.amazon.com/dp/{sku}"
    skuFolder=os.path.join(mp.sku_folder_path,sku)
    pw_page.goto(urlProducto)
    urls_images=get_urls(pw_page)
    print("\nPagina cargada en el producto "+sku)
    classificaction=get_classificaction(pw_page)
    title=get_title(pw_page)
    price=get_price(pw_page)
    overView=get_overView(pw_page)
    note=get_note(pw_page)
    technicalDetails=get_technicalDetails(pw_page)
    abaooutProduct=get_abaoutProduct(pw_page)
    otherDetails=get_otherDetails(pw_page)
    aditionalInfo=get_aditionalInfo(pw_page)
    bulletDetails=get_bulletDetails(pw_page)
    importantInfo=get_importantInfo(pw_page)
    comparitions=get_comparitions(pw_page)
    descriptions=get_descriptions(pw_page)
    garanty=get_garanty(pw_page)    
    img_down(urls_images,skuFolder)
    data={
        "sku":sku,
        "url":urlProducto,
        "clasificacion":classificaction,
        "titulo":title,
        "precio":price,
        "descripciones":descriptions,
        "Vista General":overView,
        "Detalles Tecnicos":technicalDetails,
        "Acerca del producto":abaooutProduct,
        "Otros detalles":otherDetails,
        "Contenido de la caja":bulletDetails,
        "Mas detalles Tecnicos":comparitions,
        "Informacion Importante":importantInfo,
        "Informacion Adicional":aditionalInfo,
        "Garantia":garanty,
        "Nota":note,
        "Links Imagenes":urls_images    
    }
    more_fields=get_static_fields_with_openai(data)
    data.update(more_fields)
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def remove_all_sku_folder():
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    skuFolder=os.path.join(currentFolder,"skus_Amazon")
    for sku in os.listdir(skuFolder):
        skuPath=os.path.join(skuFolder,sku)
        os.remove(skuPath)
def save_screenshot(pw_page,skuFolder):
    #create folder
    
    #validate if the folder exists
    if not os.path.exists(skuFolder):
        os.makedirs(skuFolder)
    pw_page.screenshot(path=f"{skuFolder}/screenshot.png")
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