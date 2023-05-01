#!/bin/sh

trap "pkill -P $$ -f python" TERM KILL QUIT STOP INT

cd /srv/ulf/wiki
. ./venv/bin/activate
python3.9 -m wiki
