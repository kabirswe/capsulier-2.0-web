#!/bin/bash

bower install
pip install -r src/requirements.txt | grep -v 'Requirement already satisfied'
mysql -u root "" -D web_capsulier -e "DROP DATABASE IF EXISTS web_capsulier;"
mysql -uroot -e "CREATE DATABASE web_capsulier;"
mysql -uroot -e "ALTER DATABASE web_capsulier CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -u root web_capsulier < sql/web_capsulier.sql;
python src/manage.py loaddata src/main/fixtures/admin.json
python src/manage.py runserver
