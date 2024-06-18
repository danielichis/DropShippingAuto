from playwright.sync_api import sync_playwright, expect
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from DropShippingAuto.src.utilsDropSh.readAmazon import get_product_in_amazon_carpet_parsed
from utils.managePaths import mp
from DropShippingAuto.src.marketPlacesDestino.shopify.load import LoaderShopify
from DropShippingAuto.src.marketPlacesDestino.dinners.subirInfoDinners import LoaderDinners
from DropShippingAuto.src.marketPlacesDestino.real_plaza.loadRealPlaza import LoaderRealPlaza
from DropShippingAuto.src.marketPlacesOrigen.amazon.downloadAmazon import get_sku_amazon_product
from utils.requestToGAS import post_peticion
import traceback
import json
import time
import re

from DropShippingAuto.src.marketPlacesDestino.ripley.loadRipley import LoaderRipley

class amazon_mkt_peruvians:
    def __init__(self,sheetData=None):
        self.sheetData=sheetData
        self.get_sheet_data()
        self.configDataSheet=self.sheetData['configData']
        self.product=None
        self.p = sync_playwright().start()
        user_dir=mp.get_current_chrome_profile_path()
        self.context = self.p.chromium.launch_persistent_context(user_dir,headless=False)
        self.amazonPage=self.context.pages[0]
        self.shopifyPage=self.context.new_page()
        self.dinnersPage=self.context.new_page()
        self.ripleyPage=self.context.new_page()
    def start_pages(self):
        self.go_to_amazon()
        #self.go_to_shopify()
        #self.go_to_dinners()
        self.go_to_ripley()

    def set_loaders(self):
        self.loaderDinner=LoaderDinners(dataToLoad=None,
                                  page=self.dinnersPage,
                                  sheetProductData=None,
                                  configSheetData=self.configDataSheet,
                                  context=self.context,p=self.p)
        self.loaderShopify=LoaderShopify(dataToLoad=None,
                                  page=self.shopifyPage,
                                  sheetProductData=None,
                                  configSheetData=self.configDataSheet,
                                  context=self.context,p=self.p)
        
#################  add to main flow      
        self.loaderRipley=LoaderRipley(dataToLoad=None,
                                  page=self.ripleyPage,
                                  sheetProductData=None,
                                  configSheetData=self.configDataSheet,
                                  context=self.context,
                                  p=self.p)
        
#################        
        # self.loaderRealPlaza=LoaderRealPlaza(dataToLoad=None,
        #                           page=self.realPlazaPage,
        #                           sheetProductData=None,
        #                           configSheetData=self.configDataSheet,
        #                           context=self.context,p=self.p)
        self.loadersFunctions={
            "DINNERS":self.load_to_dinners,
            "SHOPIFY":self.load_to_shopify,
            "REAL_PLAZA":self.load_to_real_plaza,
            #######
            "RIPLEY":self.load_to_ripley
            #######
        }
    def update_loaders_data(self):
        dataAmzn=get_product_in_amazon_carpet_parsed(self.product['SKU'])
        self.loaderDinner.dataToLoad=dataAmzn
        self.loaderShopify.dataToLoad=dataAmzn

        #####
        self.loaderRipley.dataToLoad=dataAmzn
        #####

        self.loaderDinner.sheetProductData=self.product
        self.loaderShopify.sheetProductData=self.product

        ####
        self.loaderRipley.sheetProductData=self.product
        ####
   


    def get_sheet_data(self):
        if self.sheetData ==None:
            print("No sheet data, leyendo localmente")
            self.sheetData=get_data_to_download()
        else:
            print("Leyendo datos de la hoja de calculo")
    def go_to_amazon(self):
        self.amazonPage.goto("https://www.amazon.com")
    def download_amazon(self):
        
        self.amazonPage.bring_to_front()
        r=get_sku_amazon_product(self.amazonPage,self.product)
        post_peticion(r)
        self.amazonDataSku=get_product_in_amazon_carpet_parsed(self.product['SKU'])
        print(r)
    def go_to_shopify(self):
        self.shopifyPage.goto(mp.newProductShopify)
        self.shopifyPage.wait_for_load_state("load")
        self.loaderShopify.handle_login_shopify()
    def go_to_dinners(self):
        self.dinnersPage.goto(mp.newProductDinners)
        self.dinnersPage.wait_for_load_state("load")
        self.loaderDinner.handle_login_dinners()
        #expect web element to be present
    def load_to_shopify(self):
        self.shopifyPage.bring_to_front()
        self.loaderShopify.load_main_sku_shopify()
        self.shopifyPage.goto(mp.newProductShopify)
        post_peticion(self.loaderShopify.responseShopifyLoad)
    def load_to_dinners(self):
        self.dinnersPage.bring_to_front()
        self.loaderDinner.load_main_dinners()
        self.dinnersPage.goto(mp.newProductDinners)
        post_peticion(self.loaderDinner.responseDinnersLoad)

    def go_to_real_plaza(self):
        self.realPlazaPage.goto(mp.newProductRealPlaza)
    def load_to_real_plaza(self):
        pass

######################add to main flow####

    def go_to_ripley(self):
        self.loaderRipley.start_playwright()
        self.loaderRipley.go_to_home()

    def load_to_ripley(self):
        self.ripleyPage.bring_to_front()  
        self.loaderRipley.load_main_ripley()  

#######################

    def main_process(self):
        self.set_loaders()
        self.start_pages()
        try:
            for product in self.sheetData['dataToLoad']:
                print(f"info de datasheet del producto {product}")
                if self.product==None or self.product['SKU']!=product['SKU']:
                    self.product=product
                    print("descargando y actualizando...")
                    self.download_amazon()
                    self.update_loaders_data()
                print(f"cargando productos...")
                self.loadersFunctions[product['MARKETPLACE']]()
        except Exception as e:
            tb=traceback.format_exc()
            self.end()
            print("Error en el proceso principal")
            print(tb)
    def end(self):
        self.context.close()
        self.p.stop()

if __name__ == "__main__":
    with open("dataToDownloadAndLoad.json","r") as f:
        sheetData=json.load(f)
    print("cargando productosSS")
    amp=amazon_mkt_peruvians(sheetData)
    amp.main_process()
    
