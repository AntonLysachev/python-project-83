install:
	poetry install --no-root

dev:
	poetry run flask --app page_analyzer:app --debug run --port 8000

PORT ?= 8000
start:
	env | sort poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

build:
	chmod +x ./build.sh; \
	./build.sh
