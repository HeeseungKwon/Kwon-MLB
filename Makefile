SHELL := /bin/bash

.PHONY: setup up ingest stream

setup:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

up:
	docker-compose up -d --build

ingest-statcast:
	python ingest/ingest_statcast.py

run-streamlit:
	streamlit run app/streamlit_app.py
