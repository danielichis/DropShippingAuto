import csv
import json
def get_data_to_download():
    #open json to load
    #DropShippingAuto\dataToDownload.json
    #DropShippingAuto\dataToDownload.json
    with open("DropShippingAuto/dataToDownload.json","r",encoding="utf-8") as json_file:
        dataLoad=json.load(json_file)
    return dataLoad

def get_product_amazon_sku(sku:str)->dict:
    #open json file
    with open("DropShippingAuto/marketPlacesOrigen/amazon/skus_Amazon","r",encoding="utf-8") as json_file:
        dataLoad=json.load(json_file)
    #filter to get the sku product
    data=[x for x in dataLoad['dataToLoad'] if x['SKU']==sku]
    return data

def test_get_product_amazon_sku():
    sku="B07QSTJV95"
    data=get_list_products_amazon_sku(sku)
    print(data)
if __name__ == "__main__":
    test_get_product_amazon_sku()