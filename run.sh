#!/bin/sh

# script to run the wiki under FreeBSD, blocks until wiki process is stopped.

# first argument of script is directory of wiki
# second argument of script is port number

# trap is executed when shell receives any signal to stop the shell.
# trap kills any python child processes, but they need to run in
# background to execute the trap (otherwise the sh process is blocked).
trap "pkill -P $$ -f python" TERM KILL QUIT STOP INT

# enter wiki directory
cd "$1"

# activate python virtual environment
. ./venv/bin/activate

# run python wiki in background
python3.9 -m wiki -p $2 &

# get pid of last started job (python)
pid=$!

# wait until python stops
wait $pid
