from flask import Flask, render_template
from flask import request, jsonify
from src.marketPlacesOrigen.amazon.downloadAmazon import download_info
from src.marketPlacesDestino.shopify.load import load_main_shopify
import json
from src.app.localApp import run_load_shopify,run_download_shopify
from src.utils.starBrowser import start_browser
from src.otrasWeb.otherWebs import got_to_amazon
from playwright.sync_api import Page,Expect


app = Flask(__name__)
@app.route('/descargar', methods=['POST'])
def run_download():
    if request.method == 'POST':
        response=None
        saveData={
            "data":request.json
        }
        with open("dataToDownload.json","w",encoding="utf-8") as json_file:
            json.dump(saveData,json_file,indent=4,ensure_ascii=False)
        
    botResponses=run_download_shopify()
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
    botResponses=run_load_shopify()
    return jsonify(botResponses)
@app.route('/')
def index():
    print("ir a google con browser abierto")
    #got_to_amazon(page)
    return "recibido"
if __name__ == '__main__':
    app.run(debug=True,port=5069)
    