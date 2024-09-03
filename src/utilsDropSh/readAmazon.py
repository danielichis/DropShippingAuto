import ast
import json
import csv
from DropShippingAuto.src.utilsDropSh.managePaths import mp
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
from utils.imgHandling.imgHandling import get_sorted_images_paths
import os
import re
from utils.structures import get_element_with_more_fields
from utils.dinamicMassivArgsExtractions_rip import dinamic_two_systems_description


def sku_folder(sku):
    return os.path.join(mp.get_current_path(1),"marketPlacesOrigen/amazon/skus_Amazon",sku)
def get_product_in_amazon_carpet_parsed(product_sku):
    skuFolder=sku_folder(product_sku)
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "r",encoding="utf-8") as f:
        dataAmazon= json.load(f)
    imagesPath=get_images_paths(product_sku)
    dataAmazon['imagesPath']=imagesPath

    return dataAmazon
 



def get_images_paths(product):
    imagesPaths_750x555=[]
    imagesPaths_1000x1000=[]
    skuFolder=sku_folder(product)
    #directories
    imagesDir_750x555=os.path.join(skuFolder,"images","resized_750x555")
    imagesDir_1000x1000=os.path.join(skuFolder,"images","resized_1000x1000")
    #sorted images paths
    imagesPaths_750x555=get_sorted_images_paths(imagesDir_750x555)
    imagesPaths_1000x1000=get_sorted_images_paths(imagesDir_1000x1000)
    imagesPaths={
        "750x555":imagesPaths_750x555,
        "1000x1000":imagesPaths_1000x1000
    }        
    return imagesPaths

def save_json(product,data):
    skuFolder=f"src/marketPlacesDestino/dinners/"
    dataJsonPath=skuFolder+f"/product_{product}.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
def get_all_products_in_amazon_carpet_parsed():
    products=get_data_to_download()
    print(len(products))
    allData_list=[]
    for product in products['dataToLoad']:
        data=get_product_in_amazon_carpet_parsed(product['SKU'])
        allData={
            "data":data
        }
        allData_list.append(allData)

    #write json file
    with open("dinnersDataToLoad.json", "w",encoding="utf-8") as f:
        json.dump(allData_list, f, indent=4, ensure_ascii=False)
    return allData_list

if __name__ == "__main__":
    r=get_product_in_amazon_carpet_parsed("B0CYL5QPN4")
    print(r['descripciones'])
    #get_all_products_in_amazon_carpet_parsed()
    pass
