import json
import csv
from DropShippingAuto.src.utils.managePaths import mp
from DropShippingAuto.src.utils.manageProducts import load_products
import os
import re
#read csv file

def sku_folder(sku):
    return os.path.join(mp.get_current_path(1),"marketPlacesOrigen\\amazon\\skus_Amazon",sku)

def load_json(product):
    skuFolder=sku_folder(product)
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "r",encoding="utf-8") as f:
        dataAmazon= json.load(f)
    vendedor="UNALUKA INTERNACIONAL"
    categoria=dataAmazon["clasificacion"]
    if "Marca" in dataAmazon['Vista General'].keys():
        marca=dataAmazon["Vista General"]["Marca"]
    elif "Marca" in dataAmazon['Detalles Tecnicos'].keys():
        marca=dataAmazon["Detalles Tecnicos"]["Marca"]
    else:
        marca="No especificado"
    sku=dataAmazon["sku"]
    nombreProducto=dataAmazon["titulo"]
    descripcionStyleds=[]
    precioAmazon=dataAmazon["precio"]
    precioAmazon = re.search(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', precioAmazon)
    precioAmazon=str(round(float(precioAmazon.group(0).replace(",","")),2))
    descriptionString=""
    if "Peso Artículo" in dataAmazon["Mas detalles Tecnicos"].keys():
        peso_libras=dataAmazon["Mas detalles Tecnicos"]["Peso Artículo"]
        peso_libras=re.findall(r"(\d+\.\d+) libras",peso_libras)[0]
        peso_kg=str(round(float(peso_libras)*0.453592,2))
    else:
        peso_kg="No especificado"
    for key,value in dataAmazon["descripciones"].items():
        descriptionString=f"{descriptionString}\n{key}:{value}"
    if "Dimensiones del artículo Largo x Ancho x Altura" in dataAmazon["Otros detalles"].keys():
        dimensions=dataAmazon["Otros detalles"]["Dimensiones del artículo Largo x Ancho x Altura"]
        largo=re.findall(r"(\d+\.\d+)",dimensions)[0]
        ancho=re.findall(r"(\d+\.\d+)",dimensions)[1]
        altura=re.findall(r"(\d+\.\d+)",dimensions)[2]
    else:
        dimensions="No especificado"
        largo_cm="25 cm"
        ancho_cm="25 cm"
        altura_cm="25 cm"

    if descriptionString=="":
        for key,value in dataAmazon["Detalles Tecnicos"].items():
            descriptionString=f"{descriptionString}\n{key}:{value}"
    
    dimensions_cm={
        "Largo cm":largo_cm,
        "Ancho cm":ancho_cm,
        "Altura cm":altura_cm,
        "peso_kg":peso_kg
    }
    imagesPath=get_images_paths(product['SKU'])
    dataToLoad={
        "vendedor":vendedor,
        "categoria":categoria,
        "marca":marca,
        "sku":sku,
        "nombreProducto":nombreProducto,
        "descripcion":descriptionString.strip(),
        "precioAmazon":precioAmazon,
        "dimensions_cm":dimensions_cm,
        "imagesPath":imagesPath
    }
    return dataToLoad

def get_images_paths(product):
    imagesPaths=[]
    skuFolder=sku_folder(product)
    imagesPath=os.path.join(skuFolder,"images")
    print(imagesPath)
    for image in os.listdir(imagesPath):
        imagesPaths.append(os.path.join(imagesPath,image))
    return imagesPaths

def save_json(product,data):
    skuFolder=f"src/marketPlacesDestino/dinners/"
    dataJsonPath=skuFolder+f"/product_{product}.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
def dinners_to_load_info():
    products=load_products()
    print(len(products))
    allData_list=[]
    for product in products['dataToLoad']:
        data=load_json(product['SKU'])
        allData={
            "data":data
        }
        allData_list.append(allData)

    #write json file
    with open("dinnersDataToLoad.json", "w",encoding="utf-8") as f:
        json.dump(allData_list, f, indent=4, ensure_ascii=False)
    return allData_list


infoDinnersToLoad=dinners_to_load_info()
if __name__ == "__main__":
    dinners_to_load_info()