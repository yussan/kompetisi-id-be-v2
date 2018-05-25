#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from app import create_app
# from dotenv import load_dotenv

# load_dotenv()

app = create_app()

if __name__  == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'])