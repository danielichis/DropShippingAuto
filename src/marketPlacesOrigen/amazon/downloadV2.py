from typing import List, Optional
from selectolax.parser import HTMLParser
from selectolax import Selector
from attrs import define, asdict
from rich import print
from playwright.sync_api import sync_playwright
import csv


@define
class Review:
    title: str | None
    helpful: str | None
    body: str | None

#form#twister div.a-row span

@define
class Item:
    code_asin: str
    title: str
    reviews: Optional[List[Review]]
    price:str
    overView:[dict]
    Note:str
    description:[str]
    technicalDetails:{str:str}
    OtherDetails:{str:str}
    aditionalInfo:{str:str}
    garanty:str
    variations:Optional[str]
    abaoutProduct:Optional[str]


def extract(html, selector, output):
    element = html.css_first(selector)
    #parent=element.parent
    if element is not None:
        if output == "text":
            return element.text(strip=True)
        elif output == "attrs":
            return element.attributes
        elif output == "listDicts":
            return element.attributes

def get_overview(html,element,selector, output):
    subelements=html.css_first(selector)

    listOverView=[]
    for subelement in subelements:
        overview={
            subelement.child:extract(subelement,"td","text")

        }



def parse_html(html):
    reviews = html.css("div[data-hook=review]")
    for review in reviews:
        yield Review(
            title=extract(review, "span[data-hook=review-title] span", output="text"),
            helpful=extract(
                review, "span[data-hook=helpful-vote-statement]", output="text"
            ),
            body=extract(review, "span[data-hook=review-body] span", output="text"),
        )


def pagination(html):
    next_page = html.css_first("li.a-last a")
    if next_page is None:
        return False


def load_products():
    with open(r"src\marketPlacesOrigen\amazon\products.csv", newline="") as f:
        reader = csv.reader(f)
        return [item[0] for item in list(reader)]


def run(asins):
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    pw_page = browser.new_page()
    for asin in asins:
        item=Item(code_asin=asin, title=None, reviews=None,price=None,overView=None,Note=None,description=None,technicalDetails=None,OtherDetails=None,aditionalInfo=None,garanty=None,variations=None,abaoutProduct=None)
        url = f"https://www.amazon.com/dp/{asin}"
        print(url)
        pw_page.goto(url)
        html = HTMLParser(pw_page.content())
        
        item.title = extract(html, "span#productTitle", "text")
        item.price=extract(html, "div#corePrice_feature_div span.a-offscreen", "text")
        item.description=extract(html, "div#productDescription span", "text")
        item.overView=extract(html, "div#productOverview_feature_div tr", "attrs")
        item.Note=extract(html, "div#universal-product-alert span", "text")
        item.technicalDetails=extract(html, "div#productDetails_techSpec_section_1 tr", "attrs")
        item.abaoutProduct=extract(html, "div#feature-bullets li span", "text")
        item.technicalDetails=extract(html, "table#productDetails_techSpec_section_1", "attrs")
        item.OtherDetails=extract(html, "table#productDetails_techSpec_section_2", "attrs")
        item.aditionalInfo=extract(html, "div#productDetails_db_sections", "attrs")
        item.garanty=extract(html, "table#productDetails_warranty_support_sections", "attrs")
        print(item.title)
    browser.close()
    pw.stop()


def main():
    total_pages = 2
    asins = load_products()
    run(asins)
    


if __name__ == "__main__":
    main()
