#!/usr/bin/python
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__  == "__main__":
    app.run(host=app.config['HOST'], port=app.config['PORT'])