#!/usr/bin/env bash
# Stop and remove all running docker containers (removes the data)
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
cd $HOME/src
cookiecutter gh:inveniosoftware/cookiecutter-invenio-instance -c v3.1 --no-input
cd my-site
docker-compose up -d
./scripts/bootstrap
./scripts/setup
./scripts/server
firefox https://127.0.0.1:5000/ &
