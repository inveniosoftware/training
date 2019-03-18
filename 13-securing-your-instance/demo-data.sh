#!/usr/bin/env bash

# Create users
pipenv run my-site users create bootcamp@test.ch -a --password=bootcamp # create user ID 2
pipenv run my-site users create captain.america@test.ch -a --password=bootcamp # create user ID 3

# Create a tokens to create records
BOOTCAMP_ACCESS_TOKEN=`pipenv run my-site tokens create -n bootcamptest -u bootcamp@test.ch`
CAPTAIN_AMERICA_ACCESS_TOKEN=`pipenv run my-site tokens create -n bootcamptest -u captain.america@test.ch`

# Record owned by bootcamp
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"My test record", "contributors": [{"name": "Doe, John"}], "owner": 1}' https://localhost:5000/api/records/?prettyprint=1 -H "Authorization: Bearer $BOOTCAMP_ACCESS_TOKEN"
# Record owned by Captain America
curl -k --header "Content-Type: application/json" --request POST --data '{"title":"Avengers secret files", "contributors": [{"name": "Copernicus, Mikolaj"}], "owner": 2}' https://localhost:5000/api/records/?prettyprint=1 -H "Authorization: Bearer $CAPTAIN_AMERICA_ACCESS_TOKEN"

echo "bootcamp@test.ch token:\nexport BOOTCAMP_ACCESS_TOKEN=$BOOTCAMP_ACCESS_TOKEN"
echo "captain.america@test.ch token:\nexport CAPTAIN_AMERICA_ACCESS_TOKEN=$CAPTAIN_AMERICA_ACCESS_TOKEN"