FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install production dependencies.
# RUN pip install Flask gunicorn
RUN pip install --no-cache-dir -r requirements.txt


# workers = プロセス数
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
# CMD exec gunicorn --bind :$PORT app:app