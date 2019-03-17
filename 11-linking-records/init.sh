#!/usr/bin/env bash
PREVIOUS=../10-linking-records

$PREVIOUS/init.sh
cp -r $PREVIOUS/solution/* ../
# ES mappings changed, need to re-run setup
../scripts/setup.sh
