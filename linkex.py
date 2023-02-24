# Imported required libs
from fastapi import FastAPI, Query
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
import re

# FastAPI Instance
app = FastAPI(
    title="Linkex",
    description="An API to extract the hyperlinks from the URLs."
)

# Data Model


class Data(BaseModel):
    urls: str

# Simple route


@app.get("/", tags=["Simple Route"])
def get_data():
    return {"message": "Hello, I am a Linkex API."}

# Link extracting route


@app.post("/", tags=["Extract Links"])
async def extract_result(route: Data):
    r = requests.get(route.urls)
    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, 'html.parser')
    anchors = [link.get("href") for link in soup.find_all(
        "a", attrs={'href': re.compile("https://")})]
    return {"Data": anchors}


# Route to extract links from pre-defined URLs using Query


@app.get("/links", tags=["Extract Data"])
async def extract_links(url: str = Query("https://geekpython.in/web-scraping-in-python-using-beautifulsoup", description="The URL to extract links from")):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = [link.get("href") for link in soup.find_all(
        "a", attrs={'href': re.compile("https://")})]
    return {"links": links}