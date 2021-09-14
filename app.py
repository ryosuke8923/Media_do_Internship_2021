import os
import requests
import random
from os.path import join, dirname
from dotenv import load_dotenv
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from flask import Flask, render_template, request
import numpy as np
import math
from mlask import MLAsk

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

TOKEN = os.environ.get("TEST")
# TOKEN = 334
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_CREDENTIALS_MANAGER = spotipy.oauth2.SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=CLIENT_CREDENTIALS_MANAGER)

APP_ID = os.environ.get("APP_ID") # applicationId(rakuten books api)

RECOMMEND_NUM = 5

RECOMMEND_PLAYLIST = {
    "6BGaNbk6J9JiPCjLAR3l3B": (-3, 4, -5, 3, 3, 0, 0, 2, 0, 5, 0),
    "5sjNdkqhmvF0RLOUwSI3AW": (1, -1, -2, 2, 0, -1, 0, -2, -3, 0),
    "0g2CExISe9gl5tCK0fGsC7": (-3, 3, 0, 0, 2, 0, 0, -2, 3, 0),
    "7eRL4exJUcTsmiNGpXR31u": (-3, 2, -5, 0, 2, 0, -3, -2, -3, 0),
    "201Vyoy07NEhcbvxVcDxCO": (2, -2, 3, 0, 0, 2, 3, 3, 3, 0),
    "78qiR2mpH9x1bAe7Bg2wjk": (-3, 3, -3, 0, 5, -3, -3, 1, 3, 0),
    "5FUKrdhKliq1eSyQP8ioZ0": (-3, 3, -1, 0, 3, 0, 0, 2, 5, 0),
    "5dQV25DPP9rfhUkOOh5VcD": (-3, 3, -3, 0, 4, -3, -3, 2, 3, 0),
    "0s4S7bzYygOGXEzF1a8c4f": (-3, 0, -3, 0, 2, 0, 0, -2, -2, 0),
    "0axQfChvnswvoQUpBTSomE": (-1, 3, -3, 0, 1, 0, 0, 1, 3, 0)
}

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

def get_songs_from_playlist(playlist_id: str):
    songs = []
    result = spotify.playlist(playlist_id)
    for item in result['tracks']['items']:
        song_name = item['track']['name']
        artist = item['track']['artists'][0]['name']
        ref = item['track']['href']
        images = item['track']['album']['images'][-1]
        # preview_url = item['track']['preview_url']
        songs.append([song_name, artist, ref, images]) # 曲名, アーティスト, URL, 画像
    if len(songs) < RECOMMEND_NUM:
        return random.sample(songs, RECOMMEND_NUM)
    else:
        return random.sample(songs, RECOMMEND_NUM)

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