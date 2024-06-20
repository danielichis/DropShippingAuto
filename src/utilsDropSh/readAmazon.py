import json
import csv
from DropShippingAuto.src.utilsDropSh.managePaths import mp
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from DropShippingAuto.src.otrasWeb.scrapUpc import get_upc
import os
import re

from utils.structures import get_element_with_more_fields
#read csv file

def sku_folder(sku):
    #return os.path.join(mp.get_current_path(1),"marketPlacesOrigen\\amazon\\skus_Amazon",sku)
    return os.path.join(mp.get_current_path(1),"marketPlacesOrigen/amazon/skus_Amazon",sku)
def get_product_in_amazon_carpet_parsed(product_sku):
    skuFolder=sku_folder(product_sku)
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "r",encoding="utf-8") as f:
        dataAmazon= json.load(f)
    vendedor="UNALUKA INTERNACIONAL"
    categoria=dataAmazon["clasificacion"]
    if "Marca" in dataAmazon['Vista General'].keys():
        dataAmazon['Marca']=dataAmazon["Vista General"]["Marca"]
    elif "Marca" in dataAmazon['Detalles Tecnicos'].keys():
        dataAmazon['Marca']=dataAmazon["Detalles Tecnicos"]["Marca"]
    else:
        marca="No especificado"
    sku=dataAmazon["sku"]
    try:
        precioAmazon=dataAmazon["precio"]
        precioAmazon = re.search(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', precioAmazon)
        precioAmazon=str(round(float(precioAmazon.group(0).replace(",","")),2))
        dataAmazon['precio']=precioAmazon
    except:
        precioAmazon="no especificado"
    descriptionString=""
    if "Peso Artículo" in dataAmazon["Mas detalles Tecnicos"].keys():
        peso_libras=dataAmazon["Mas detalles Tecnicos"]["Peso Artículo"]
        peso_libras=re.findall(r"(\d+\.\d+) libras",peso_libras)[0]
        peso_kg=str(round(float(peso_libras)*0.453592,2))
        dataAmazon['Peso Kg']=peso_kg
    else:
        peso_kg="200"
    list_descripciones=[dataAmazon["descripciones"],dataAmazon["Vista General"],dataAmazon["Acerca del producto"],dataAmazon["Detalles Tecnicos"]]
    print(list_descripciones)
    dataAmazon["descripciones"]=get_element_with_more_fields(list_descripciones)
    
    # el que tenga mas elementos 


    if "Dimensiones del artículo Largo x Ancho x Altura" in dataAmazon["Otros detalles"].keys():
        dimensions=dataAmazon["Otros detalles"]["Dimensiones del artículo Largo x Ancho x Altura"]
        largo=re.findall(r"(\d+\.\d+)",dimensions)[0]
        ancho=re.findall(r"(\d+\.\d+)",dimensions)[1]
        altura=re.findall(r"(\d+\.\d+)",dimensions)[2]
    else:
        dimensions="No especificado"
        largo_cm="25"
        ancho_cm="25"
        altura_cm="25"

    dimensions_cm={
        "Largo cm":largo_cm,
        "Ancho cm":ancho_cm,
        "Altura cm":altura_cm,
        "peso_kg":peso_kg
    }
    dataAmazon['dimensions_cm']=dimensions_cm
    imagesPath=get_images_paths(product_sku)
    dataAmazon['imagesPath']=imagesPath
    dataAmazon['upc']=get_upc(product_sku)

    return dataAmazon

def get_images_paths(product):
    imagesPaths=[]
    skuFolder=sku_folder(product)
    imagesPath=os.path.join(skuFolder,"images")
    print(imagesPath)
    for image in os.listdir(imagesPath):
        #cambio
        if os.path.splitext(image)[1] == '.jpg':
            #cambio
            imagesPaths.append(os.path.join(imagesPath,image))
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
    r=get_product_in_amazon_carpet_parsed("B000GAYQJ0")
    print(r['descripciones'])
    #get_all_products_in_amazon_carpet_parsed()
    pass