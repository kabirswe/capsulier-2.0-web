#!/bin/bash

python src/manage.py migrate
python src/manage.py runserver
