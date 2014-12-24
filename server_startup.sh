#!/bin/bash
WORKDIR=.
export WORKDIR
#PYTHONPATH=$PYTHONPATH:/root
PYTHONPATH=$PYTHONPATH:WORKDIR
PYTHONPATH=$PYTHONPATH:$WORKDIR/jobs/refine
export PYTHONPATH
python ./startup.py
python ./tools/mapper_watcher.py &
