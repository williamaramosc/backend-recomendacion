import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books = pd.read_csv('datos/books.csv', encoding = "ISO-8859-1", usecols=['book_id', 'goodreads_book_id','title','authors','average_rating', 'original_publication_year', 'ratings_count', 'language_code','image_url'])
print(books.head())

book_tags = pd.read_csv('datos/book_tags.csv', encoding = "ISO-8859-1")
print(book_tags.head())

tags = pd.read_csv('datos/tags.csv')
print(tags.tail())

tags_join_DF = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')
print(tags_join_DF.head())
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(books['authors'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Build a 1-dimensional array with book titles
titles = books['title']
indices = pd.Series(books.index, index=books['title'])

# Function that get book recommendations based on the cosine similarity score of book authors
def authors_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]

authors_recommendations('The Hobbit').head(20)

books_with_tags = pd.merge(books, tags_join_DF, left_on='goodreads_book_id', right_on='goodreads_book_id', how='inner')

tf1 = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix1 = tf1.fit_transform(books_with_tags['tag_name'].head(10000))
cosine_sim1 = linear_kernel(tfidf_matrix1, tfidf_matrix1)   

# Build a 1-dimensional array with book titles
titles1 = books['title']
indices1 = pd.Series(books.index, index=books['title'])

# Function that get book recommendations based on the cosine similarity score of books tags
def tags_recommendations(title):
    idx = indices1[title]
    sim_scores = list(enumerate(cosine_sim1[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    return titles.iloc[book_indices]

tags_recommendations('The Hobbit').head(20)

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

print(corpus_recommendations("The Hobbit"))
