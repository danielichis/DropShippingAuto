from flask import Flask, render_template
from flask import request, jsonify
from src.marketPlacesOrigen.amazon.downloadAmazon import download_info
from src.marketPlacesDestino.shopify.load import load_main_shopify
import json
app = Flask(__name__)
@app.route('/descargar', methods=['POST'])
def run_donload():
    if request.method == 'POST':
        response=None
        saveData={
            "data":request.json
        }
        with open("dataToDownload.json","w",encoding="utf-8") as json_file:
            json.dump(saveData,json_file,indent=4,ensure_ascii=False)
        
        print("descagando informacion de amazon")
        with open("dataToDownload.json","r",encoding="utf-8") as json_file:
            data=json.load(json_file)

        dr=download_info(data['data']['dataToLoad'])
        #lr=load_main_shopify(data['data'])
        botResponses=[]
        for i,r in enumerate(dr):
            botResponse={
                **r,
                **data['data']['dataToLoad'][i]
            }
            botResponses.append(botResponse)
    with open("Responsedata_download.json","w",encoding="utf-8") as json_file:
        json.dump(botResponses,json_file,indent=4,ensure_ascii=False)

    return jsonify(botResponses)

@app.route('/load', methods=['POST'])
def run_load():
    if request.method == 'POST':
        response=None
        saveData={
            "data":request.json
        }
        with open("dataToLoad.json","w",encoding="utf-8") as json_file:
            json.dump(saveData,json_file,indent=4,ensure_ascii=False)
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
        with open("Responsedata_load.json","w",encoding="utf-8") as json_file:
            json.dump(botResponses,json_file,indent=4,ensure_ascii=False)
    return jsonify(botResponses)
if __name__ == '__main__':
    app.run(debug=True,port=5069)
    