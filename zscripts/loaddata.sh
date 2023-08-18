#!/bin/bash

python src/manage.py loaddata src/main/fixtures/auth_user.json
python src/manage.py loaddata src/main/fixtures/site.json
python src/manage.py loaddata src/main/fixtures/db.json
python src/manage.py loaddata src/userprofile/fixtures/db.json
python src/manage.py loaddata src/product/fixtures/db.json
python src/manage.py loaddata src/page/fixtures/db.json
python src/manage.py loaddata src/blog/fixtures/db.json
python src/manage.py loaddata src/mycaps/fixtures/db.json
python src/manage.py loaddata src/eshop/fixtures/db.json
