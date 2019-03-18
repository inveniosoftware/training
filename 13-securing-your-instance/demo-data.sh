#!/usr/bin/env bash

# Create users
pipenv run my-site users create admin@test.ch -a --password=123456 # create admin user ID 1
pipenv run my-site users create manager@test.ch -a --password=123456 # create admin user ID 2
pipenv run my-site users create visitor@test.ch -a --password=123456 # create visitor user ID 3

# Create an admin token to create records
ADMIN_ACCESS_TOKEN=`pipenv run my-site tokens create -n bootcamptest -u admin@test.ch`

# Record owned by admin
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"My test record", "contributors": [{"name": "Doe, John"}], "owner": 1}' https://localhost:5000/api/records/?prettyprint=1 -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN"
# Record owned by managern
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"Second test record", "contributors": [{"name": "Copernicus, Mikolaj"}], "owner": 2}' https://localhost:5000/api/records/?prettyprint=1 -H "Authorization: Bearer $ADMIN_ACCESS_TOKEN"
# Visitor does not have access to any record
