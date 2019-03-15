# Developing with Invenio

## Useful commands:

Set up environment variable for debug mode
```commandline
export FLASK_DEBUG=1
```

Run docker services
```commandline
docker-compose up
```

Build documentation
```commandline
python setup.py build_sphinx
```

Initialize git repo
```commandline
git init
```

Stage changes for commit
```commandline
git add --all
```

Update manifest file
```commandline
check-manifest update
```

### Testing

Run tests
```commandline
./run-tests
```

Enable E2E testing
```commandline
export E2E="yes"
export E2E_WEBDRIVER_BROWSERS="Chrome Firefox"
```

Add your browser driver to `$PATH` (temporarily)
```commandline
export PATH=<path_to_parent_directory_of_the_driver>:$PATH
```

### Scripts:

Initialise database from scratch
```commandline
./scripts/setup
```

Build project assets, (re)install dependencies
```commandline
./scripts/bootstrap
```

Run invenio server (if $FLASK_DEBUG=1 server refreshes on change of the code)
```commandline
./scripts/server
```



### Pipenv

Installing python dependencies (updated as Pipfile indicates)
```commandline
pipenv sync --dev
```

Activate virtualenv
```commandline
pipenv shell
```

### Troubleshooting
To kill and remove all docker containers
```commandline
docker stop $(docker ps -a -q); docker rm $(docker ps -a -q)
```

