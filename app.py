import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import sys

from flask import Flask, render_template, request

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

TOKEN = os.environ.get("TEST")
# TOKEN = 334

APP_ID = os.environ.get("APP_ID") # applicationId(rakuten books api)

@app.route('/')
def hello_world():
    ver = sys.version
    # target = os.environ.get('TARGET', 'World')
    return render_template('index.html')

# "/" →　"〇〇.html"の結果表示のとこへ変更する
@app.route("/result.html",methods=["POST"])
def show():
    title = request.form["title"]
    return render_template('result.html',title=title)

@app.route('/about')
def aboutPage():
    return render_template('about.html')

def get_books_by_title(title: str):
    url = "https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404"
    params = {
                "format": "json",
                "applicationId": APP_ID,
                "title": title
             }
    r = requests.get(url, params=params)
    return r.json()

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8888)))