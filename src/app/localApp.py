
from src.marketPlacesOrigen.amazon.downloadAmazon import download_info
from src.marketPlacesDestino.shopify.load import load_main_shopify
import json

def run_download_shopify():
    with open("dataToDownload.json","r",encoding="utf-8") as json_file:
        data=json.load(json_file)
    dr=download_info(data['data']['dataToLoad'])
    botResponses=[]
    for i,r in enumerate(dr):
        botResponse={
            **r,
            **data['data']['dataToLoad'][i]
        }
        botResponses.append(botResponse)
        with open("Responsedata_download.json","w",encoding="utf-8") as json_file:
            json.dump(botResponses,json_file,indent=4,ensure_ascii=False)
    return botResponses
def run_load_shopify():
    with open("dataToLoad.json","r",encoding="utf-8") as json_file:
        dataLoad=json.load(json_file)
        lr=load_main_shopify(dataLoad['data'])
        botResponses=[]
        for i,r in enumerate(lr):
            botResponse={
                **r,
                **dataLoad['data']['dataToLoad'][i]
            }
            botResponses.append(botResponse)
        print(botResponses)
        with open("Responsedata_load.json","w",encoding="utf-8") as json_file:
            json.dump(botResponses,json_file,indent=4,ensure_ascii=False)
    return botResponses
if __name__ == '__main__':
    run_download_shopify()
    run_load_shopify()