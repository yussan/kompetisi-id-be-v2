#Kompetisi Indonesia Api v2

## Prerequisites
- Python https://www.python.org/downloads/
- Pip https://pypi.python.org/pypi/pip 
- MySQL https://www.mysql.com/downloads/

## Install
```
pip install -r requirements.txt
```
or install from virtualenv
```
./venv/bin/pip install -r requirements.txt
```

## Run
```
./run.sh
```

## Configuration
Set the following configuration to the environment variable
```
# environtment
ENV=<string> default = development, production

# mysql config
DB_HOST=<string>
DB_NAME=<string>
DB_PORT=<string> default = 3306

#flask
DEBUG=<boolean> default = True
```

## Documentation 
https://documenter.getpostman.com/view/100843/RW87q9og