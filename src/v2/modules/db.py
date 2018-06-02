from sqlalchemy import create_engine
import os

# database init
# solved from : https://stackoverflow.com/questions/22252397/importerror-no-module-named-mysqldb
db_host = os.environ.get('DB_HOST', 'db4free.net')
db_user = os.environ.get('DB_USER', 'root42')
db_password = os.environ.get('DB_PASSWORD', 'Rahasia42_')
db_name = os.environ.get('DB_NAME', 'ki_dev42')

# solved utf8 from: https://stackoverflow.com/questions/11972363/sqlalchemy-and-unicodedecodeerror?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
engine = create_engine('mysql+pymysql://' + db_user + ':' + db_password + '@' + db_host + '/' + db_name + '?charset=utf8', pool_recycle=3600)
# print executed query

# log option
engine.echo = os.environ.get('FLASK_DEBUG') == 'True' or os.environ.get('FLASK_DEBUG') == True
connection = engine.connect()
connection = connection.execution_options(
    isolation_level="READ COMMITTED"
)