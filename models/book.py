from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Float, Integer, String
from config.database import meta, engine

# Modelo de usuario en el cual se crea la tabla en la base de datos
books = Table("books", meta, Column("book_id", Integer, primary_key=True),
              Column("goodreads_book_id", Integer, primary_key=True),
              Column("authors", String(512)),
              Column("original_publication_year", Integer),
              Column("title", String(512)),
              Column("average_rating", Float),
              Column("ratings_count", Integer),
              Column("language_code", String(50)),
              Column("image_url", String(1024)))

meta.create_all(engine)
