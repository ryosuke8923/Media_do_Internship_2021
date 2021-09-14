import os
import requests
from os.path import join, dirname
from dotenv import load_dotenv
import sys

from flask import Flask, render_template, request
import numpy as np
import math
from mlask import MLAsk

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

TOKEN = os.environ.get("TEST")
# TOKEN = 334

APP_ID = os.environ.get("APP_ID") # applicationId(rakuten books api)

#分析(analyzer,feature)
analyzer = MLAsk()
features = ["iya","yorokobi","kowa","yasu","suki","aware","ikari","odoroki","takaburi","haji",]

#本の感情をベクトルに変換
def change_vector(dic):
  vector = []
  for feature in features:
    vector.append(dic[feature])
  return vector

#本の感情分析
def sentiment_analyze(outline):
  sentiment_dic = {}
  result = analyzer.analyze(outline)
  emotion = result["emotion"]
  if emotion != None:
    for feature in features:
      if emotion[feature] == None:
        sentiment_dic[feature] == 0
      else:
        sentiment_dic[feature] = len(emotion[feature])
  book_vector = change_vector(sentiment_dic)
  return book_vector

#本とカテゴリの類似度計算
def calulate_cos(book,category):
  x = np.dot(book,category)
  a = math.sqrt(sum(list(map(lambda x: x**2,book)))+0.01)
  b = math.sqrt(sum(list(map(lambda x: x**2,category)))+0.01)
  category_vector = x / (a*b)
  return category_vector


@app.route('/')
def hello_world():
    ver = sys.version
    # target = os.environ.get('TARGET', 'World')
    return render_template('index.html')

# "/" →　"〇〇.html"の結果表示のとこへ変更する
@app.route("/result.html",methods=["POST"])
def show():
    title = request.form["title"]
    #楽天APIにタイトル名を渡す.
    book = get_books_by_title(title)
    outline = ""
    #感情分析を行う．
    book_vector = sentiment_analyze(outline)
    #本とカテゴリの類似度計算
    cos = 0
    for category in categories:
        cos = max(cos,calulate_cos(book,category))
    #spotify APIから音楽データをとってくる        
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