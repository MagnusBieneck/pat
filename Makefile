##########################
#    Makefile for pat    #
# (c)2019 Magnus Bieneck #
##########################
SHELL := /bin/bash


##################################### I N I T   T A R G E T S #####################################
init.marker: setup.py
	pip install -e .[install]
	touch init.marker
init: init.marker
.PHONY: init


################################# D J A N G O   M A N A G E . P Y #################################
run: init
	python manage.py runserver
.PHONY: run


makemigrations: init
	python manage.py makemigrations
.PHONY: makemigrations


migrate: init
	python manage.py migrate
.PHONY: migrate


##################################### T E S T   T A R G E T S #####################################
lint: init
	pylint pat/* refund/* tests/*
.PHONY: lint


test: init
	pytest --cov-config .coveragerc --cov=./ --cov-report term-missing:skip-covered tests --cov-fail-under=90
.PHONY: test


quick-verify: lint test
.PHONY: quick-verify


##################################### C L E A N   T A R G E T #####################################
clean:
	rm -rf *.marker pat.egg-info/* build/* dist/*
