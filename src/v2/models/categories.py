from ..modules.db import connection
from sqlalchemy import Table, Column, MetaData, select, update, func, BIGINT, INT, DATETIME, TEXT, or_

metadata = MetaData()

# main category table declaration
MainCategory = Table('main_kat', metadata,
                     Column('id_main_kat', BIGINT),
                     Column('main_kat', TEXT),
                     Column('color', TEXT),
                     Column('logo', TEXT),
                     Column('deskripsi', TEXT)
                     )

# sub category table declaration
SubCategory = Table('sub_kat', metadata,
                    Column('id_sub_kat', BIGINT),
                    Column('id_main_kat', BIGINT),
                    Column('sub_kat', TEXT)
                    )

# function to get list competition categories and sub categories
def getMainCategories():
    query = select([MainCategory.c.id_main_kat, MainCategory.c.main_kat, MainCategory.c.deskripsi, MainCategory.c.color])
    result = connection.execute(query).fetchall()
    return result 

# function to get sub categories by main category id
def getSubCategories(main_category_id):
    query = select([SubCategory.c.id_sub_kat, SubCategory.c.sub_kat]).where(SubCategory.c.id_main_kat == main_category_id)
    result = connection.execute(query).fetchall()
    return result