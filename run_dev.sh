#!/usr/bin/env bash
export $(cat .env) && cd ./venv/bin && source activate && cd ../../ && python3 ./src/run.py