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

start

    ./wiki.py
