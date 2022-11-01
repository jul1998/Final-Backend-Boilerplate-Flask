rm -R -f ./migrations &&
mysql -u root -e "DROP DATABASE example;" &&
mysql -u root -e "CREATE DATABASE example;" &&
pipenv run init &&
pipenv run migrate &&
pipenv run upgrade