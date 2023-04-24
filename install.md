# Installation

make sure python3, pip, virtualenv and pandoc is installed. maybe some xml libraries also need to be installed for html sanitization.

cd into wiki directory

create virtual environment

    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install -U -r requirements.txt
    mkdir sources

start

    ./wiki.py

