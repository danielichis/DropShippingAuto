from playwright.sync_api import sync_playwright
import json
import requests
import io
from tqdm import tqdm
import os
from PIL import Image
import csv

def load_products():
    with open(r"products.csv", newline="") as f:
        reader = csv.reader(f)
        return [item[0] for item in list(reader)]
def get_overView(pw_page):
    overView=pw_page.query_selector_all("div#productOverview_feature_div tr")
    overVies=[]
    for view in overView:
        overVies.append({
            view.query_selector("td:nth-child(1) span").inner_text():view.query_selector("td:nth-child(2) span").inner_text().replace("\u200e","")
        })
    return overVies

def get_technicalDetails(pw_page):
    technicalDetails=pw_page.query_selector_all("table#productDetails_techSpec_section_1 tr")
    technicalDetailsList=[]
    for technicalDetail in technicalDetails:
        technicalDetailsList.append({
            technicalDetail.query_selector("th:nth-child(1)").inner_text():technicalDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
        })
    return technicalDetailsList

def get_abaoutProduct(pw_page):
    abaoutProduct=pw_page.query_selector_all("div#feature-bullets li span")
    abaoutProductList=[]
    for abaoutProduct in abaoutProduct:
        abaoutProductList.append(abaoutProduct.inner_text())
    return abaoutProductList

def get_otherDetails(pw_page):
    otherDetails=pw_page.query_selector_all("table#productDetails_techSpec_section_2 tr")
    otherDetailsList=[]
    for otherDetail in otherDetails:
        otherDetailsList.append({
            otherDetail.query_selector("th:nth-child(1)").inner_text():otherDetail.query_selector("td:nth-child(2)").inner_text().replace("\u200e","")
        })
    return otherDetailsList

def get_aditionalInfo(pw_page):
    aditionalInfo=pw_page.query_selector_all("div#productDetails_db_sections tr")
    aditionalInfoList=[]
    for aditionalInfo in aditionalInfo:
        aditionalInfoList.append({
            aditionalInfo.query_selector("th:nth-child(1)").inner_text():aditionalInfo.query_selector("td:nth-child(2)").inner_text()
        })
    return aditionalInfoList
def get_bulletDetails(pw_page):
    bulletInfo=pw_page.query_selector_all("div#detailBullets_feature_div li")
    bulletInfoList=[]
    for bullet in bulletInfo:
        bulletInfoList.append({
            bullet.query_selector("span span").inner_text():bullet.query_selector("span:nth-child(2)").inner_text()
        })
    return bulletInfoList

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
def img_down(links,skuImageFolder):
    for link in links:
        response  = requests.get(link).content 
        image_file = io.BytesIO(response)
        image  = Image.open(image_file)
        imagePath=skuImageFolder+"/"+link.split('/')[-1]
        with open(imagePath , "wb") as f:
            image.save(f , "JPEG")

def download_sku(pw_page,sku,urlProducto,skuFolder):
    pw_page.goto(urlProducto)
    print("\nPagina cargada en el producto "+sku)
    classificaction=pw_page.locator("div#wayfinding-breadcrumbs_feature_div li span[class=a-list-item]").all_inner_texts()
    title=pw_page.query_selector("span#productTitle").inner_text()
    price=pw_page.query_selector("div#corePrice_feature_div span.a-offscreen").inner_text()
    try:
        descriptions=pw_page.query_selector("div#productDescription span").inner_text()
    except:
        descriptions=None
    overView=get_overView(pw_page)
    try:
        note=pw_page.query_selector("div#universal-product-alert span:nth-child(2)").inner_text()
    except:
        note=None
    technicalDetails=get_technicalDetails(pw_page)
    abaooutProduct=get_abaoutProduct(pw_page)
    otherDetails=get_otherDetails(pw_page)
    aditionalInfo=get_aditionalInfo(pw_page)
    bulletDetails=get_bulletDetails(pw_page)
    importantInfo=get_importantInfo(pw_page)

    try:
        garanty=pw_page.query_selector("h1.a-size-medium.a-spacing-small.secHeader+div>span:nth-child(3)").inner_text()
    except:
        garanty=None

    urls=get_urls(pw_page)
    skuImageFolder=skuFolder+"/images"
    os.makedirs(skuFolder)
    os.makedirs(skuImageFolder)
    img_down(urls,skuImageFolder)
    data={
        "url":urlProducto,
        "classificaction":classificaction,
        "title":title,
        "price":price,
        "descriptions":descriptions,
        "overView":overView,
        "note":note,
        "technicalDetails":technicalDetails,
        "abaooutProduct":abaooutProduct,
        "otherDetails":otherDetails,
        "bulletDetails":bulletDetails,
        "importantInfo":importantInfo,
        "aditionalInfo":aditionalInfo,
        "garanty":garanty,
        "imageUrls":urls    
    }
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
def remove_all_sku_folder():
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    skuFolder=os.path.join(currentFolder,"skus_Amazon")
    for sku in os.listdir(skuFolder):
        skuPath=os.path.join(skuFolder,sku)
        os.remove(skuPath)
def download_info():
    products=load_products()
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context=browser.new_context(storage_state="state.json")
    pw_page = context.new_page()
    for sku in tqdm(products):
        urlProducto=f"https://www.amazon.com/dp/{sku}"
        currentFolder = os.path.dirname(os.path.abspath(__file__))
        skuFolder=currentFolder+"/skus_Amazon/"+sku
        if not os.path.exists(skuFolder):
            download_sku(pw_page,sku,urlProducto,skuFolder)
        else:
            print("el producto ya existe")
    context.close()
    browser.close()
    pw.stop()
if __name__ == "__main__":
    download_info()
