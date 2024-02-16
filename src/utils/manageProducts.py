import csv
import json
def load_products():
    #open json to load
    with open("dataToLoad.json","r",encoding="utf-8") as json_file:
        dataLoad=json.load(json_file)
    return dataLoad