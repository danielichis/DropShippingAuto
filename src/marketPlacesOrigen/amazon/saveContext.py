from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time

print("iniciando en la hora" + time.strftime("%H:%M:%S", time.localtime()))
p= sync_playwright().start()
browser = p.chromium.launch()
context=browser.new_context(storage_state="state.json")
page=context.new_page()
urlProducto="https://www.amazon.com/dp/B08ZJQVV6G/?m=ATVPDKIKX0DER&_encoding=UTF8&tag=edealinfocom-20&linkCode=ur2&camp=1789&creative=9325&th=1"

page.goto(urlProducto)
html = HTMLParser(page.content())
print("html obtenido")
print("obteniendo html de la pagina en el tiempo" + time.strftime("%H:%M:%S", time.localtime()))
#storage = context.storage_state(path="state.json")
page.goto(urlProducto)
html = HTMLParser(page.content())
print("obteniendo html de la pagina en el tiempo" + time.strftime("%H:%M:%S", time.localtime()))
page.close()
context.close()
browser.close()
p.stop()