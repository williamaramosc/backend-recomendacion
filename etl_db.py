import pandas as pd
import numpy as np
from sqlalchemy import create_engine

DATABASE_URL = "mysql+mysqlconnector://root123:root123@35.238.124.195:3306/baserecomendacion"
engine = create_engine(DATABASE_URL, echo=False)

libros_df=pd.read_sql("SELECT * FROM books", DATABASE_URL)
print(libros_df.head(5))
ratings_df=pd.read_csv("datos/ratings.csv")
book_tags = pd.read_csv('datos/book_tags.csv', encoding = "ISO-8859-1")
tags = pd.read_csv('datos/tags.csv')

def crearUsuarios():
    nombres ={'Sergio', 'Carlos', 'William', 'Steven', 'Hernan', 'Daniel', 'Miguel', 'John'}

    arraya = ratings_df['user_id'].unique()
    arraya = sorted(arraya)
    b = pd.DataFrame(arraya, columns=['user_id'])
    c = pd.DataFrame(columns=['name'])
    c['name'] = np.random.choice(list(nombres), b.shape[0])
    b = b.join(c['name'])
    b.to_sql(name='users', con=engine, if_exists='append', index=False)

def guardarLibros():
    libros_df.to_sql(name='books', con=engine, if_exists='append', index=False)

def guardarRating():
    #ratings_df.to_sql(name='ratings', con=engine, if_exists='append', index=False)
    split_df = np.array_split(ratings_df, 50)
    for dataf in split_df:
        dataf.to_sql(name='ratings', con=engine, if_exists='append', index=False)

def guardarBookTag():
    #book_tags.sort_values('count', ascending=False).drop_duplicates(subset=['goodreads_book_id', 'tag_id'])
    nuevoBook = book_tags.drop(209)
    nuevoBook = nuevoBook.drop(159371)
    nuevoBook = nuevoBook.drop(265128)
    nuevoBook = nuevoBook.drop(265140)
    nuevoBook = nuevoBook.drop(265155)
    nuevoBook = nuevoBook.drop(265187)
    nuevoBook = nuevoBook.drop(308767)
    nuevoBook = nuevoBook.drop(308771)
    nuevoBook.to_sql(name='books_tag', con=engine, if_exists='append', index=False)

def guardarTags():
    tags.to_sql(name='tags',con=engine, if_exists='append', index=False)







