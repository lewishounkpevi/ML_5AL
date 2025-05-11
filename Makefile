SHELL := /bin/bash

install-venv:
	python3.11 -m venv .cours-ml && pwd

# source .cours-ml/bin/activate

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt


format:
	black *.py maison/*.py maison/connexion/*.py maison/data_management/*.py maison/autres/*.py


lint:
	pylint --disable=R,C *.py maison/*.py maison/connexion/*.py maison/data_management/*.py maison/autres/*.py
knit:
	quarto preview "/home/lewis/formation/modelisation/Rapport_auto2.qmd" --no-browser --no-watch-inputs

install-pkg:
	cd . &&\
	pip install dist/maison-0.1-py3-none-any.whl --force-reinstall

compile-pkg:
	cd . &&\
		python setup.py sdist bdist_wheel

clean:
	rm -rf .cours_ml
	find -iname "*.pyc" -delete
	
	
all: install-venv install format lint clean