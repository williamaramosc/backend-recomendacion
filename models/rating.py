from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import meta, engine

# Modelo de rating en el cual se crea la tabla en la base de datos
ratings = Table("ratings", meta, Column("user_id", Integer, primary_key=True), 
                           Column("book_id", Integer, primary_key=True),
                           Column("rating", Integer))

meta.create_all(engine)
