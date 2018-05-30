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
                    Column('sub_kat', TEXT)
                    )
