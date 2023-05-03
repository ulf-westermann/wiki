#!/bin/sh

# trap is executed when shell receives any signal to stop the shell.
# trap kills any python child processes, but they need to run in
# background to execute the trap (otherwise the sh process is blocked).
trap "pkill -P $$ -f python" TERM KILL QUIT STOP INT

# enter wiki directory
cd /srv/ulf/wiki

# activate python virtual environment
. ./venv/bin/activate

# run python wiki in background
python3.9 -m wiki &

# get pid of last started job (python)
pid=$!

# wait until python stops
wait $pid
