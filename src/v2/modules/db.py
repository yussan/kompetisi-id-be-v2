from sqlalchemy import create_engine
import os

# database init
# solved from : https://stackoverflow.com/questions/22252397/importerror-no-module-named-mysqldb
db_host = os.environ.get('DB_HOST', 'localhost')
db_user = os.environ.get('DB_USER', 'root')
db_password = os.environ.get('DB_PASSWORD', 'rahasia')
db_name = os.environ.get('DB_NAME', 'ki')

engine = create_engine('mysql+pymysql://' + db_user + ':' + db_password + '@' + db_host + '/' + db_name, pool_recycle=3600)
# print executed query
engine.echo = True
connect = engine.connect()