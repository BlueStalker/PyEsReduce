#!/bin/bash
PYTHONPATH=$PYTHONPATH:/root
PYTHONPATH=$PYTHONPATH:/root/refine
PYTHONPATH=$PYTHONPATH:/root/refine/jobs/refine
export PYTHONPATH
python ./startup.py
python ./tools/mapper_watcher.py &
