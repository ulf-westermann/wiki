#!/bin/sh

# trap is executed when shell receives any signal that stops the shell.
# trap kills any child python processes, but they need to run in background
# to execute the trap.
trap "pkill -P $$ -f python" TERM KILL QUIT STOP INT

cd /srv/ulf/wiki # enter wiki directory
. ./venv/bin/activate # activate python virtual environment
python3.9 -m wiki & # run python wiki in background
pid=$! # get pid of last started job (python)
wait $pid # wait until python stops
