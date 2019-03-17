#!/usr/bin/env bash
PREVIOUS=../09-deposit-form

$PREVIOUS/init.sh
cp -r $PREVIOUS/solution/* ../
cd ../
# entrypoints changed, need to re-install the app
pipenv run pip install -e .
