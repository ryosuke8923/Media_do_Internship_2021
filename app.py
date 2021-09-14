import os
from os.path import join, dirname
from dotenv import load_dotenv
import sys

from flask import Flask, render_template, request

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

TOKEN = os.environ.get("TEST")
# TOKEN = 334

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

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8888)))