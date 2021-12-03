from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer
from config.database import meta, engine

# Modelo de usuario en el cual se crea la tabla en la base de datos
books_tag = Table("books_tag", meta, Column("goodreads_book_id", Integer, primary_key=True),
                  Column("tag_id", Integer, primary_key=True),
                  Column("count", Integer))

meta.create_all(engine)
