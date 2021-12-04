import pandas as pd

import numpy as np

from typing import Optional

from fastapi import FastAPI, Request

from pydantic import BaseModel

from routes.routes import user

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import linear_kernel

from scipy.stats import pearsonr

import mysql.connector

from sqlalchemy import create_engine

from typing import List

import json

DATABASE_URL = "mysql+mysqlconnector://root123:root123@35.238.124.195:3306/baserecomendacion"

engine = create_engine(DATABASE_URL, echo=False)

class Rating(BaseModel):
    user_id: int
    book_id: int
    rating: int

class ListaRating(BaseModel):
    __root__: List[Rating]

class Libro(BaseModel):
    book_id: int
    goodreads_book_id: int
    authors: str
    original_publication_year: int
    title: str
    average_rating: float
    ratings_count: int
    language_code: str
    image_url: str
    
class ListaLibros(BaseModel):
    libros: list[Libro]

app = FastAPI()

app.include_router(user)

libros_df=pd.read_sql("SELECT * FROM books", DATABASE_URL)
book_tags = pd.read_sql("SELECT * FROM books_tag", DATABASE_URL)
tags = pd.read_sql("SELECT * FROM tags", DATABASE_URL)

def getRatings(id):
    sql = "SELECT books.book_id, books.goodreads_book_id, books.authors, books.original_publication_year, books.title, ratings.rating, books.language_code, books.image_url FROM users, ratings, books WHERE users.user_id = "+str(id)+" and users.user_id = ratings.user_id and ratings.book_id = books.book_id"
    ratings = pd.read_sql(sql, DATABASE_URL)
    return ratings

def getRatingsColab(id):
    sql = "SELECT books.title, ratings.rating FROM users, ratings, books WHERE users.user_id = " +str(id)+ " and users.user_id = ratings.user_id and ratings.book_id = books.book_id"
    lista = pd.read_sql(sql, DATABASE_URL)
    return lista

def recomendacionColaborativa(id):
    sql = "SELECT * from ratings"
    ratings_df=pd.read_sql(sql, DATABASE_URL)
    lista = getRatingsColab(id)
    mi_lista = lista

    lista_usuario = pd.merge(mi_lista, libros_df, on='title', how='inner')
    lista_usuario = lista_usuario[['book_id', 'title', 'rating']].sort_values(by='book_id')

    otros_usuarios = ratings_df[ratings_df['book_id'].isin(lista_usuario['book_id'].values)]
    otros_usuarios['user_id'].nunique()

    usuarios_mutuos = otros_usuarios.groupby(['user_id'])
    usuarios_mutuos = sorted(usuarios_mutuos, key=lambda x: len(x[1]), reverse=True)

    usuarios_comunes = usuarios_mutuos[:100]

    pearson_corr = {}

    for user_id, libros in usuarios_comunes:
        libros = libros.sort_values(by='book_id')
        lista_libros = libros['book_id'].values

        libros
        lista_libros

        ratings_nuevos = lista_usuario[lista_usuario['book_id'].isin(lista_libros)]['rating'].values
        ratings_usuario = libros[libros['book_id'].isin(lista_libros)]['rating'].values

        corr = pearsonr(ratings_nuevos, ratings_usuario)
        pearson_corr[user_id] = corr[0]

    pearson_df = pd.DataFrame(columns=['user_id', 'indice_de_similaridad'], data=pearson_corr.items())
    pearson_df = pearson_df.sort_values(by='indice_de_similaridad', ascending=False)[:50]

    ratings_comunes = pearson_df.merge(ratings_df, on='user_id', how='inner')
    ratings_comunes['rating_ponderado'] = ratings_comunes['rating'] * ratings_comunes['indice_de_similaridad']

    rating_global = ratings_comunes.groupby('book_id').sum()[['indice_de_similaridad','rating_ponderado']]

    recomendaciones = pd.DataFrame()

    recomendaciones['puntaje_promedio_recomendacion'] = rating_global['rating_ponderado']/rating_global['indice_de_similaridad']
    recomendaciones['book_id'] = rating_global.index
    recomendaciones = recomendaciones.reset_index(drop=True)

    recomendaciones = recomendaciones[(recomendaciones['puntaje_promedio_recomendacion'] == 5)]

    recomendados = libros_df[libros_df['book_id'].isin(recomendaciones['book_id'])][['book_id']].head(50)

    recomendados = pd.merge(recomendados, libros_df, on="book_id")

    return recomendados

@app.get("/librosPopulares")
async def leer_libros():
    libros = libros_df
    libro = libros.head(100)
    data = libro.to_json(orient='records')
    parsed = json.loads(data)
    return parsed

@app.get("/recomendadosColab/{user_id}")
async def recomendacionColab(user_id: int):
    libros = recomendacionColaborativa(user_id)
    libro = libros.head(100)
    data = libro.to_json(orient="records")
    parsed = json.loads(data)
    return parsed    

@app.get("/todos")
async def todos_libros():
    libros = libros_df
    data = libros.to_json(orient='records')
    parsed = json.loads(data)
    return parsed

@app.get("/librosUsuario/{user_id}")
async def libros_usuario(user_id: int):
    lista = getRatings(user_id)
    data = lista.to_json(orient="records")
    parsed = json.loads(data)
    return parsed

@app.post("/login/{user_id}")
async def login(user_id: int):
    sql = "select * from users where user_id = "+str(user_id)
    usuario = pd.read_sql(sql, DATABASE_URL)

    if(usuario.empty == True):
        return{"user_id" : 0}
    else:
        return{"user_id":user_id}


@app.post("/usuarioNuevo")
async def usuario_nuevo(lista: ListaRating):
    lista1 = ListaRating.parse_obj(lista)
    print(lista1)
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"items":{"item_id": item_id, "q": q}}

def recomendacionContenido(paramTitle):
    books = libros_df

    tags_join_DF = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')

    books_with_tags = pd.merge(books, tags_join_DF, left_on='goodreads_book_id', right_on='goodreads_book_id', how='inner')

    indices1 = pd.Series(books.index, index=books['title'])

    temp_df = books_with_tags.groupby('goodreads_book_id')['tag_name'].apply(' '.join).reset_index()
    temp_df.head()

    books = pd.merge(books, temp_df, left_on='goodreads_book_id', right_on='goodreads_book_id', how='inner')

    books.head()

    books['corpus'] = (pd.Series(books[['authors', 'tag_name']]
                    .fillna('')
                    .values.tolist()
                    ).str.join(' '))

    tf_corpus = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
    tfidf_matrix_corpus = tf_corpus.fit_transform(books['corpus'])
    cosine_sim_corpus = linear_kernel(tfidf_matrix_corpus, tfidf_matrix_corpus)

    # Build a 1-dimensional array with book titles
    titles = books['title']
    indices = pd.Series(books.index, index=books['title'])

    # Function that get book recommendations based on the cosine similarity score of books tags
    def corpus_recommendations(title):
        idx = indices1[title]
        sim_scores = list(enumerate(cosine_sim_corpus[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:21]
        book_indices = [i[0] for i in sim_scores]
        return titles.iloc[book_indices]

    return corpus_recommendations(paramTitle)

