from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import meta, engine

# Modelo de usuario en el cual se crea la tabla en la base de datos
users = Table("users", meta, Column("user_id", Integer, primary_key=True), 
                           Column("name", String(255)))

meta.create_all(engine)
