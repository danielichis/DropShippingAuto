
from src.marketPlacesOrigen.amazon.downloadAmazon import download_info
from src.marketPlacesDestino.shopify.load import load_main_shopify
import json

def run_bot():
    with open("data.json","r",encoding="utf-8") as json_file:
        data=json.load(json_file)
    dr=download_info(data['data']['dataToLoad'])
    lr=load_main_shopify(data['data'])
    botResponses=[]
    for i,r in enumerate(dr):
        botResponse={
            **r,
            **lr[i]
        }
        botResponses.append(botResponse)
    return botResponses
if __name__ == '__main__':
    run_bot()
    