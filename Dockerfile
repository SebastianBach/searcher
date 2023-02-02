FROM python:3.8-slim-buster


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY apps/ /app/apps
COPY searcher/ /app/searcher

WORKDIR /app/apps/web/

CMD [ "python3", "web.py", "/data", "/resources"]
