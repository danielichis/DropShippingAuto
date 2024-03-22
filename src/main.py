#inicializar navegador
#descargar producto

#cargar en shopify
#cargar en dinners
#cargar en real plaza
#cargar en ripley
#cargar en mercado libre

from playwright.sync_api import sync_playwright
from DropShippingAuto.src.utilsDropSh.manageProducts import get_data_to_download
from utils.managePaths import mp
from DropShippingAuto.src.marketPlacesDestino.shopify.load import load_main_sku_shopify
from DropShippingAuto.src.marketPlacesOrigen.amazon.downloadAmazon import get_sku_amazon_product
import json
import time
newProductDinners="https://admin.quickcomm.co/catalog/products"
newProductShopify="https://admin.shopify.com/store/unaluka/products/new"
newProductRealPlaza="https://inretail.mysellercenter.com/#/dashboard"
import re

class amazon_mkt_peruvians:
    def __init__(self,sheetData=None):
        self.sheetData=sheetData
        self.get_sheet_data()
        self.p = sync_playwright().start()
        user_dir=mp.get_current_chrome_profile_path()
        self.context = self.p.chromium.launch_persistent_context(user_dir,headless=False)
        self.amazonPage=self.context.pages[0]
        self.shopifyPage=self.context.new_page()
        # self.dinnersPage=self.context.new_page()
        # self.realPlazaPage=self.context.new_page()
    def get_sheet_data(self):
        if self.sheetData ==None:
            print("No sheet data, leyendo localmente")
            self.sheetData=get_data_to_download()
        else:
            print("Leyendo datos de la hoja de calculo")
    def go_to_amazon(self):
        self.amazonPage.goto("https://www.amazon.com")
    def download_amazon(self):
        r=get_sku_amazon_product(self.amazonPage,self.product)
        print(r)
    def go_to_shopify(self):
        self.shopifyPage.goto(newProductShopify)
    def load_to_shopify(self):
        load_main_sku_shopify(self.shopifyPage,self.product,configData=self.sheetData['configData'])
        self.shopifyPage.goto(newProductShopify)
    def go_to_dinners(self):
        self.dinnersPage.goto(newProductDinners)
    def load_to_dinners(self):
        pass
    def go_to_real_plaza(self):
        self.realPlazaPage.goto(newProductRealPlaza)
    def load_to_real_plaza(self):
        pass

    def main_process(self):
        self.go_to_shopify()
        self.go_to_amazon()
        for product in self.sheetData['dataToLoad']:
            self.product=product
            self.download_amazon()
            self.load_to_shopify()
            # self.load_to_dinners()
            # self.load_to_real_plaza()

    def end(self):
        self.context.close()
        self.p.stop()

if __name__ == "__main__":
    amp=amazon_mkt_peruvians()
    amp.main_process()
    #amp.go_to_amazon()
    # amp.go_to_shopify()
    # amp.load_to_shopify()
    # amp.go_to_dinners()
    # amp.go_to_real_plaza()
    print("cargando producto")
    #amp.download_amazon(prductSample)

