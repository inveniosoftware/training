#!/usr/bin/env bash
exercises="
05-customizing-invenio
07-data-models-new-field
08-data-models-from-scratch
09-deposit-form
10-indexing-records
11-linking-records
12-managing-access
"

exercise_tutorial_folder=$1
echo $exercises | grep -qw "$exercise_tutorial_folder"
valid_exercise=$?

if [ $valid_exercise -ne 0 ]
then
    echo "$exercise_tutorial_folder does not exists or it does not have a solution folder."
    exit 1
fi

invenio_src_folder="$HOME/src"
invenio_training_folder="$invenio_src_folder/training"
invenio_instance_folder="$invenio_src_folder/my-site"

if [ -d "$invenio_instance_folder" ]
then
    echo 'Removing previous Invenio instance folder.'
    rm -rf "$invenio_instance_folder"
fi
cd "$invenio_src_folder"

# Bootstrap Invenio instance
echo "Boostrapping Invenio on $invenio_instance_folder."
cookiecutter gh:inveniosoftware/cookiecutter-invenio-instance -c master --no-input

# Reinstalling appliation with preivious steps solutions
cp -R "$invenio_training_folder/$exercise_tutorial_folder/solution/my-site/*" "$invenio_instance_folder"
echo "Reinstalling application."
cd "$invenio_instance_folder"
pipenv run pip install -e .

# Start Invenio instance
docker-compose up -d
./scripts/bootstrap
./scripts/setup
./scripts/server
