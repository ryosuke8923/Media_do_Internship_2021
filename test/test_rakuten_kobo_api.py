import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

APP_ID = os.environ.get("APP_ID")

def book_search(title):
    url = "https://app.rakuten.co.jp/services/api/Kobo/EbookSearch/20170426"
    params = {
                "format": "json",
                "language": "JA",
                "applicationId": APP_ID,
                "title": title
             }
    r = requests.get(url, params=params)
    assert r.status_code == 200

if __name__ == '__main__':
    book_search("キングダム")
