import requests
from selectolax.parser import HTMLParser
import re
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download

def get_upc_from_upcitemdb(sku):
    upcItemdbUrl = "https://www.upcitemdb.com/"
    url = f"{upcItemdbUrl}/upc/{sku}"
    r=requests.get(url)
    html=HTMLParser(r.content)
    if html.css_first("div[class='rImage'] a"):
        upc=html.css_first("div[class='rImage'] a").text()
    else:
        upc="Not found"
    response={
        "web":"upcitemdb",
        "sku":sku,
        "upc":upc
    }
    print(response)
    return response

def get_upc_from_barcode_index(sku):
    barcodeIndexUrl = "https://barcodeindex.com/"
    url = f"{barcodeIndexUrl}search?q={sku}"
    r=requests.get(url)
    #print(r.text)
    html=HTMLParser(r.content)
    if html.css_first("h2[class]"):
        upc=html.css_first("h2[class]").text()
        upc=re.findall(r"(\d+)",upc)[0]
    else:
        upc="Not found"
    response={
        "web":"barcodeIndex",
        "sku":sku,
        "upc":upc
    }
    print(response)
    return response

def get_upc(sku):
    upc=get_upc_from_barcode_index(sku)
    if upc["upc"]=="Not found":
        upc=get_upc_from_upcitemdb(sku)
    if upc["upc"]=="Not found":
        upc["upc"]="-"
    return upc["upc"]

def test_skus():
    skus=get_data_to_download()
    for sku in skus:
        get_upc_from_barcode_index(sku)
        get_upc_from_upcitemdb(sku)