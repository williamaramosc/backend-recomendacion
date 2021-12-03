from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.database import meta, engine

# Modelo de usuario en el cual se crea la tabla en la base de datos
tags = Table("tags", meta, Column("tag_id", Integer, primary_key=True),
             Column("tag_name", String(512)))
meta.create_all(engine)
