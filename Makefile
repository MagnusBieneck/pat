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
run: init compilemessages
	python manage.py runserver
.PHONY: run


makemigrations: init
	python manage.py makemigrations
.PHONY: makemigrations


migrate: init
	python manage.py migrate
.PHONY: migrate


makemessages: init
	python manage.py makemessages
.PHONY: makemessages


compilemessages: init locale/de/LC_MESSAGES/django.po
	python manage.py compilemessages
.PHONY: compilemessages


##################################### T E S T   T A R G E T S #####################################
lint: init
	pylint pat/* refund/* tests/*
.PHONY: lint


test: init test-unit test-integration
.PHONY: test


test-unit: init
	pytest --cov-config .coveragerc-unit --cov=./ --cov-report term-missing:skip-covered tests/unit --cov-fail-under=100
.PHONY: test-unit


test-integration: init
	pytest --cov-config .coveragerc-integration --cov=./ --cov-report term-missing:skip-covered tests/integration --cov-fail-under=100
.PHONY: test-integration


quick-verify: lint test
.PHONY: quick-verify


##################################### C L E A N   T A R G E T #####################################
clean:
	rm -rf *.marker pat.egg-info/* build/* dist/* locale/*/LC_MESSAGES/*.mo geckodriver.log
