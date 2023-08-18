#!/bin/bash

python src/manage.py dumpdata auth.user --indent 2 > src/main/fixtures/auth_user.json
python src/manage.py dumpdata sites --indent 2 > src/main/fixtures/site.json
python src/manage.py dumpdata main --indent 2 > src/main/fixtures/db.json
python src/manage.py dumpdata userprofile --indent 2 > src/userprofile/fixtures/db.json
python src/manage.py dumpdata product --indent 2 > src/product/fixtures/db.json
python src/manage.py dumpdata page --indent 2 > src/page/fixtures/db.json
python src/manage.py dumpdata blog --indent 2 > src/blog/fixtures/db.json
python src/manage.py dumpdata mycaps --indent 2 > src/mycaps/fixtures/db.json
python src/manage.py dumpdata eshop --indent 2 > src/eshop/fixtures/db.json
