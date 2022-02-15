# Prerequisites

To be able to participate in the workshop exercises that will take place, you
will have to have a basic setup of development tools on your machine. We have
prepared a variety of solutions for you to achieve this setup.

Which solution should I use? It depends :-)

- **VirtualBox:** Good for in-person workshops. Ensures coherent setup for all
  participants, and makes life easier for trainers.
- **Local setup:** Good for new developers. Ensures your environment is ready
  doing development after having completed the tutorials.
- **Vagrant:** Similar to VirtualBox, but requires to also have Vagrant
  installed.

## VirtualBox (for workshops)

1. [Install VirtualBox](https://www.virtualbox.org/wiki/Downloads) for your
   platform
2. Download the OVA file from
   <https://inveniosoftware.web.cern.ch/inveniosoftware/download/virtualbox/Invenio%20Bootcamp%20Ubuntu%202019.ova> (~3GB)
3. Open the VirtualBox application and go to "File -> Import Appliance..." and
   select the downloaded OVA file from the previous step. Proceed with clicking
   "Next" and then "Import".
4. After the appliance has been loaded, it will appear in the list of Virtual
   Machines as "Invenio Bootcamp Ubuntu"
5. Double click the entry to start the VM
6. The username/password for the user is `bootcamp`/`bootcamp`

## Local setup (for new developers)

For a local development setup, make sure that you have:

* A modern IDE that supports Python, e.g. VSCode, Sublime, Atom, PyCharm etc.
* Git
* Python 3.6+
* [`pip`](https://pip.pypa.io) and [`pipenv`](https://pipenv.readthedocs.io)
  installed and fully working
* [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/installation.html)
  for scaffolding
* NodeJS version 14+ and NPM ([see official
  installaion](https://nodejs.org/en/download/))
* [Docker](https://docs.docker.com/install/) and [Docker
  Compose](https://docs.docker.com/compose/install/)
* [Google Chrome](https://www.google.com/chrome/) and
  [ChromeDriver](http://chromedriver.chromium.org/getting-started) for E2E
  tests
* If running Linux/MacOS you'll have to bump your `vm.max_map_count` as
  described in [Elasticsearch
  docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)

If you're running Ubunut/Debian you can run `sudo bootstrap.sh $(whoami)` to
install some of the above. Feel free to look inside the `bootstrap.sh` script
to understand/adjust what is installed/changed.

## Vagrant (if you know what you're doing)

1. [Download and install Vagrant](https://www.vagrantup.com/downloads.html) for
   your platform.
2. Run the following:

```bash
# Clone this repository
git clone git@github.com:inveniosoftware/training.git
cd training/00-prerequisites

# Bring up the Vagrant VM
vagrant up
# ...wait for the setup to finish...

# SSH to the VM
vagrant ssh
```
