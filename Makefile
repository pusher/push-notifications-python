# Makefile for pusher_push_notifications
all: run

venv:
	rm -rf venv
	python3 -m virtualenv venv
	venv/bin/pip3 install -Ur requirements.txt
	venv/bin/pip3 install -Ur dev_requirements.txt

venv_2:
	rm -rf venv
	python2.7 -m virtualenv venv
	venv/bin/pip install -Ur requirements.txt
	venv/bin/pip install -Ur dev_requirements.txt

check: test

test: venv
	@venv/bin/python -m nose -s

lint: venv
	@venv/bin/python -m pylint ./pusher_push_notifications/*.py
	@venv/bin/python setup.py checkdocs
