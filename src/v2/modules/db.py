from sqlalchemy import create_engine

# database init
# solved from : https://stackoverflow.com/questions/22252397/importerror-no-module-named-mysqldb
db = create_engine('mysql+pymysql://root:rahasia@localhost/ki', pool_recycle=3600)
# print executed query
db.echo = True
connect = db.connect()