# Installation

make sure python3, pip, virtualenv and pandoc is installed.

cd into wiki directory

create virtual environment

    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install -U -r requirements.txt

activate wanted plugins by creating symlinks:

    mkdir plugins
    cd plugins
    ln -s ../plugin_repository/links.py
    cd ..

start (manually / for development)

    ./wiki.py


# Initial Setup

Open webbrowser, navigate to `http://<wiki base url>/manage/`.

Click on "new" button.

Create new default page with name "index.md". Enter content in the edit field, click "store" button.

If you want CSS styles, do the same for any number of "\*.css" files, which you reference from your markdown files.


# Update

cd into wiki directory (as 'freebsd' user)

    git pull
    su
    service wikixxx stop
    service wikixxx start

where 'xxx' is 'ulf' or 'reine' respectively

