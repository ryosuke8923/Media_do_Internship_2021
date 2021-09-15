FROM python:3.7

RUN apt update
RUN apt-get install git

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
# RUN pip install Flask gunicorn
RUN pip install --no-cache-dir -r requirements.txt


RUN apt-get install -y libmecab-dev \
                        mecab \
                        mecab-ipadic \
                        mecab-ipadic-utf8 \
                        build-essential

RUN pip install mecab

RUN git clone https://github.com/hiraikiichi/team_c.git
ENV FLASK_APP /app/team_c/app.py
CMD flask run -h 0.0.0.0 -p $PORT

    # workers = プロセス数
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
# CMD exec gunicorn --bind :$PORT app:app