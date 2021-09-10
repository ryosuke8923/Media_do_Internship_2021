import os
import sys

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    ver = sys.version
    # target = os.environ.get('TARGET', 'World')
    return 'Hello!{}\n'.format(ver)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8888)))