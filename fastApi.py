from fastapi import FastAPI
from src.utils.starBrowser import start_browser
from src.otrasWeb.otherWebs import got_to_amazon
from playwright.sync_api import Page,Expect

page=start_browser()
app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/amazon")
async def amazon():
    got_to_amazon(page)
    return {"message": "Hello World"}