import time
from playwright.sync_api import sync_playwright
import json
import requests
import io
from tqdm import tqdm
import os
from src.utils.manageProducts import load_products
from src.utils.managePaths import pathsManager
from PIL import Image
import csv

def get_overView(pw_page):
    overView=pw_page.query_selector_all("div[id='productOverview_feature_div'] div[class='a-section a-spacing-small a-spacing-top-small']>div")
    overVies={}
    for view in overView:
        try:
            overVies[view.query_selector("span:nth-child(1)").inner_text()]=view.query_selector("span:nth-child(2)").inner_text().replace("\u200e","")
        except:
            pass
    return overVies

def get_technicalDetails(pw_page):
    technicalDetails=pw_page.query_selector_all("table#productDetails_techSpec_section_1 tr")
    technicalDetailsDict={}
    for technicalDetail in technicalDetails:
        technicalDetailsDict[technicalDetail.query_selector("th:nth-child(1)").inner_text()]=technicalDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
    return technicalDetailsDict

def get_abaoutProduct(pw_page):
    abaoutProduct=pw_page.query_selector_all("div#feature-bullets li span")
    abaoutProductDict={}
    if len(abaoutProduct)>0:
        for abaoutP in abaoutProduct:
            try:
                ab1=abaoutP.inner_text().split(":")[0]
                ab2=abaoutP.inner_text().split(":")[1]
                abaoutProductDict[ab1]=ab2
            except:
                pass    
    return abaoutProductDict

def get_otherDetails(pw_page):
    otherDetails=pw_page.query_selector_all("table#productDetails_techSpec_section_2 tr")
    otherDetailsDict={}
    for otherDetail in otherDetails:
        otherDetailsDict[otherDetail.query_selector("th:nth-child(1)").inner_text()]=otherDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
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
        bulletInfoDict[bullet.query_selector("span span").inner_text()]=bullet.query_selector("span:nth-child(2)").inner_text()
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
        response  = requests.get(link).content 
        image_file = io.BytesIO(response)
        image  = Image.open(image_file)
        sku=link.split('/')[-1]
        imagePath=os.path.join(skuImageFolder,sku)
        with open(imagePath , "wb") as f:
            image.save(f , "JPEG")
def get_comparitions(pw_page):
    rows=pw_page.query_selector_all("table[id='HLCXComparisonTable'] tr[class='comparison_other_attribute_row']")
    comparisonDict={}
    for row in rows:
        comparisonDict[row.query_selector("th span").inner_text()]=row.query_selector("td:nth-child(2) span").inner_text()
    return comparisonDict
def get_descriptions(pw_page):
    descriptions=pw_page.query_selector("div#productDescription span")
    if descriptions:
        list_Descs=descriptions.inner_text().split("\n\n")
    else:
        list_Descs=[]
    dicDescs={}
    for desc in list_Descs:
        print("texto en linea: "+desc)
        try:
            d1=desc.split(":")[0]
            d2=desc.split(":")[1]
            dicDescs[d1]=d2
        except:
            pass
    return dicDescs
def get_classificaction(pw_page):
    classificaction=pw_page.locator("div#wayfinding-breadcrumbs_feature_div li span[class=a-list-item]").all_inner_texts()
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

def download_sku(pw_page,sku,urlProducto,skuFolder):
    pw_page.goto(urlProducto)
    print("\nPagina cargada en el producto "+sku)
    pw_page.wait_for_selector("div#wayfinding-breadcrumbs_feature_div li span[class=a-list-item]")

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
    urls_images=get_urls(pw_page)
    img_down(urls_images,skuFolder)
    data={
        "sku":sku,
        "url":urlProducto,
        "classificaction":classificaction,
        "title":title,
        "price":price,
        "descriptions":descriptions,
        "overView":overView,
        "technicalDetails":technicalDetails,
        "abaooutProduct":abaooutProduct,
        "otherDetails":otherDetails,
        "bulletDetails":bulletDetails,
        "comparitions":comparitions,
        "importantInfo":importantInfo,
        "aditionalInfo":aditionalInfo,
        "garanty":garanty,
        "note":note,
        "imageUrls":urls_images    
    }
    
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    # data to txt file
    dataTxtPath=skuFolder+"/data.txt"
    with open(dataTxtPath, "w",encoding="utf-8") as f:
        f.write(f"sku:{sku}\n")
        f.write(f"url:{urlProducto}\n")
        f.write(f"title:{title}\n")
        f.write(f"price:{price}\n")
        f.write(f"garanty:{garanty}\n")
        f.write(f"note:{note}\n")
        f.write(f"classificaction:{classificaction}\n")
        f.write("---------------------------------------\n")
        f.write(f"descriptions:{descriptions}\n")
        f.write("---------------------------------------\n")
        f.write(f"overView:{overView}\n")
        f.write("---------------------------------------\n")
        f.write(f"technicalDetails:{technicalDetails}\n")
        f.write("---------------------------------------\n")
        f.write(f"abaooutProduct:{abaooutProduct}\n")
        f.write("---------------------------------------\n")
        f.write(f"otherDetails:{otherDetails}\n")
        f.write("---------------------------------------\n")
        f.write(f"bulletDetails:{bulletDetails}\n")
        f.write("---------------------------------------\n")
        f.write(f"comparitions:{comparitions}\n")
        f.write("---------------------------------------\n")
        f.write(f"importantInfo:{importantInfo}\n")
        f.write("---------------------------------------\n")
        f.write(f"aditionalInfo:{aditionalInfo}\n")


def remove_all_sku_folder():
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    skuFolder=os.path.join(currentFolder,"skus_Amazon")
    for sku in os.listdir(skuFolder):
        skuPath=os.path.join(skuFolder,sku)
        os.remove(skuPath)
def save_screenshot(pw_page,skuFolder):
    #create folder
    os.makedirs(skuFolder)
    pw_page.screenshot(path=f"{skuFolder}/screenshot.png")
def download_info():
    products=load_products()
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
    context=browser.new_context(storage_state="state.json")
    pw_page = context.new_page()
    for sku in tqdm(products):
        urlProducto=f"https://www.amazon.com/dp/{sku}"
        currentFolder =os.path.join(pathsManager.get_current_path(1),"marketPlacesOrigen","amazon")
        skuFolder=os.path.join(currentFolder,"skus_Amazon",sku)
        if not os.path.exists(skuFolder):
            # try:
            download_sku(pw_page,sku,urlProducto,skuFolder)
            # except Exception as e:
            #     print(e)
            #     save_screenshot(pw_page,skuFolder)
        else:
            print("el producto ya existe")
    context.close()
    browser.close()
    pw.stop()
if __name__ == "__main__":
    download_info()
    #print(os.path.join(pathsManager.get_current_path(1),"marketPlacesOrigen","amazon"))