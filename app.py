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
@app.route("/",methods=["POST"])
def show():
    title = request.form["title"]
    return "ようこそ、" + title + "さん"

@app.route('/about')
def aboutPage():
    return render_template('about.html')

def get_books_by_title(title: str):
    url = "https://app.rakuten.co.jp/services/api/Kobo/EbookSearch/20170426"
    params = {
                "format": "json",
                "language": "JA",
                "applicationId": APP_ID,
                "title": title
             }
    r = requests.get(url, params=params)
    # とりあえず1つだけ返す
    for item in r.json()['Items']:
        title = item['Item']['title']
        image = item['Item']['smallImageUrl']
        author = item['Item']['author']
        review = item['Item']['reviewAverage']
        publish_name = item['Item']['publisherName']
        return [title, image, author, review, publish_name] # タイトル, 画像, 作者, 評価(5点満点), レーベル
    return # 検索結果なし

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8888)))