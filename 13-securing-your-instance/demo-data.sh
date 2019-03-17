#!/usr/bin/env bash

# Create users
my-site users create admin@test.ch -a --password=123456 # create admin user ID 1
my-site users create manager@test.ch -a --password=123456 # create admin user ID 2
my-site users create visitor@test.ch -a --password=123456 # create visitor user ID 3

# Record owned by admin
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"My test record", "contributors": [{"name": "Doe, John"}], "owner": 1}' https://localhost:5000/api/records/?prettyprint=1
# Record owned by managern
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"Second test record", "contributors": [{"name": "Copernicus, Mikolaj"}], "owner": 2}' https://localhost:5000/api/records/?prettyprint=1
# Visitor does not have access to any record
