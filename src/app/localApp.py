
from DropShippingAuto.src.marketPlacesOrigen.amazon.downloadAmazon import download_info
from DropShippingAuto.src.marketPlacesDestino.shopify.load import load_main_shopify
import json

def run_download_amazon():
    with open("DropShippingAuto/dataToDownload.json","r",encoding="utf-8") as json_file:
        data=json.load(json_file)
    dr=download_info(data['dataToLoad'])
    botResponses=[]
    for i,r in enumerate(dr):
        botResponse={
            **r,
            **data['dataToLoad'][i]
        }
        botResponses.append(botResponse)
    with open("DropShippingAuto/Responsedata_download.json","w",encoding="utf-8") as json_file:
        json.dump(botResponses,json_file,indent=4,ensure_ascii=False)
    return botResponses
def run_load_shopify():
    with open("DropShippingAuto/dataToLoad.json","r",encoding="utf-8") as json_file:
        dataLoad=json.load(json_file)
        lr=load_main_shopify(dataLoad)
        botResponses=[]
        for i,r in enumerate(lr):
            botResponse={
                **r,
                **dataLoad['dataToLoad'][i]
            }
            botResponses.append(botResponse)
        print(botResponses)
        with open("DropShippingAuto/Responsedata_load.json","w",encoding="utf-8") as json_file:
            json.dump(botResponses,json_file,indent=4,ensure_ascii=False)
    return botResponses
if __name__ == '__main__':
    #run_download_amazon()
    run_load_shopify()