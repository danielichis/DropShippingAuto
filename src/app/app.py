from flask import Flask, render_template
from flask import request, jsonify
from src.marketPlacesOrigen.amazon.downloadAmazon import download_info
from src.marketPlacesDestino.shopify.load import load_main_shopify
import json
app = Flask(__name__)
@app.route('/ejecutarBot', methods=['POST'])
def run_bot():
    if request.method == 'POST':
        response=None
        saveData={
            "data":request.json
        }
        with open("data.json","w",encoding="utf-8") as json_file:
            json.dump(saveData,json_file,indent=4,ensure_ascii=False)
        
        print("descagando informacion de amazon")
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
    with open("Responsedata.json","w",encoding="utf-8") as json_file:
        json.dump(saveData,json_file,indent=4,ensure_ascii=False)
        
        return jsonify(botResponses)
if __name__ == '__main__':
    app.run(debug=True,port=5069)
    