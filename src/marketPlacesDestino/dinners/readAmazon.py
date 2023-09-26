import json
import csv
from src.utils.managePaths import src_path
from src.utils.manageProducts import load_products
import os
import re
#read csv file

def sku_folder(sku):
    return os.path.join(src_path,"marketPlacesOrigen\\amazon\\skus_Amazon",sku)

def load_json(product):
    skuFolder=sku_folder(product)
    dataJsonPath=skuFolder+"/data.json"
    with open(dataJsonPath, "r",encoding="utf-8") as f:
        dataAmazon= json.load(f)
    vendedor="UNALUKA INTERNACIONAL"
    categoria=dataAmazon["classificaction"]
    marca=dataAmazon["overView"]["Marca:"]
    sku=dataAmazon["sku"]
    nombreProducto=dataAmazon["title"]
    descripcionStyleds=[]
    for description in dataAmazon["abaooutProduct"]:
        try:
            d1=description.split(":")[0]
            d2=description.split(":")[1]
            descripcionStyled="<b>"+d1+"</b>"+":"+d2
            descripcionStyleds.append(descripcionStyled)
        except:
            pass
    descripcion="\n\n".join(descripcionStyleds)
    precioBase=dataAmazon["price"]

    dimensions=dataAmazon["otherDetails"]["Dimensiones del artículo Largo x Ancho x Altura"]
    largo=re.findall(r"(\d+\.\d+)",dimensions)[0]
    ancho=re.findall(r"(\d+\.\d+)",dimensions)[1]
    altura=re.findall(r"(\d+\.\d+)",dimensions)[2]

    largo_cm=round(float(largo)*2.54,2)
    ancho_cm=round(float(ancho)*2.54,2)
    altura_cm=round(float(altura)*2.54,2)
    dimensions_cm={
        "Largo cm":largo_cm,
        "Ancho cm":ancho_cm,
        "Altura cm":altura_cm
    }
    dataToLoad={
        "vendedor":vendedor,
        "categoria":categoria,
        "marca":marca,
        "sku":sku,
        "nombreProducto":nombreProducto,
        "descripcion":descripcion,
        "precioBase":precioBase,
        "dimensions_cm":dimensions_cm,
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
    dataJsonPath=skuFolder+"/product.json"
    with open(dataJsonPath, "w",encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
def main():
    products=load_products()
    print(len(products))
    for product in products:
        imagesPath=get_images_paths(product)
        data=load_json(product)
        allData={
            "imagesPath":imagesPath,
            "data":data
        }
    save_json(product,allData)
    return allData
infoAmazon=main()