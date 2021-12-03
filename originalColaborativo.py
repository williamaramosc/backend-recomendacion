import pandas as pd
import numpy as np

libros_df=pd.read_csv("datos/books.csv")
ratings_df=pd.read_csv("datos/ratings.csv")

lista = {'Of Mice and Men': 5,
            'Pet Sematary': 4,
            '1984': 5,
            'Fahrenheit 451': 4
            }

mi_lista = pd.DataFrame(columns=['title', 'rating'], data=lista.items())

lista_usuario = pd.merge(mi_lista, libros_df, on='title', how='inner')
lista_usuario = lista_usuario[['book_id', 'title', 'rating']].sort_values(by='book_id')

otros_usuarios = ratings_df[ratings_df['book_id'].isin(lista_usuario['book_id'].values)]
otros_usuarios['user_id'].nunique()

usuarios_mutuos = otros_usuarios.groupby(['user_id'])
usuarios_mutuos = sorted(usuarios_mutuos, key=lambda x: len(x[1]), reverse=True)

usuarios_comunes = usuarios_mutuos[:100]

from scipy.stats import pearsonr

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

recomendados = libros_df[libros_df['book_id'].isin(recomendaciones['book_id'])][['book_id']]
print(recomendados.shape[0])
