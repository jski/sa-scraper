# sa-scraper
Scraper to stream a thread to a webhook easily.

## Prerequisites
* Python3
* Docker

## Setup .env file
* ```threadid```
* ```webhook_url```

## For non-Docker use
```
virtualenv venv
./venv/scripts/Activate
pip install -r requirements.txt
python main.py
```

## For Docker use:
```
docker-compose build
docker-compose up -d
```
