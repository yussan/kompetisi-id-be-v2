#!/usr/bin/env bash
export $(cat .env)  && ./venv/bin/python ./src/run.py