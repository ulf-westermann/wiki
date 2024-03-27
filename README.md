# Wiki

A minimalist (and ugly) personal wiki/content management system. It contains it own integrated webserver, but it is recommended to use a reverse proxy if it is exposed to the public internet. Websites are written in [Pandoc](https://pandoc.org/MANUAL.html#pandocs-markdown) markdown.


## Installation

Make sure Python3, pip, virtualenv and pandoc is installed.

cd into wiki directory

Create virtual environment

    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install -U -r requirements.txt

Activate selected plugins by creating symlinks:

    mkdir plugins
    cd plugins
    ln -s ../plugin_repository/links.py
    cd ..

Start (manually/for development)

    ./wiki.py

Optional: create service to run the wiki.


## Initial Setup

Open webbrowser, navigate to `http://<wiki base url>/manage/`.

Click on "new" button.

Create new default page with name "index.md". Enter content in the edit field, click "store" button.

If you want CSS styles, do the same for any number of "\*.css" files, which you reference from your markdown files.

