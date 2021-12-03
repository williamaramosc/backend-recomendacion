from fastapi import APIRouter, Response
from config.database import conn
from models.user import users
from schemas.user import User
from models.rating import ratings
from schemas.rating import Rating
from models.book import books
from schemas.book import Book
from models.book_tag import books_tag
from schemas.book_tag import Book_Tag
from models.tag import tags
from schemas.tag import Tag
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()

# ======================================USUARIO=========================================
# Obtener todos los usuarios de tabla User
@user.get("/getUsers")
def get_users():
    return conn.execute(users.select()).fetchall()

# Obtener un usuario en especifico de la tabla User
@user.get("/getUser/{id}")
def get_user(id: str):
    return conn.execute(users.select().where(users.c.user_id == id)).first()
    
# Agregar un usuario
@user.post("/postUsers")
def create_user(user: User):
    new_user = {"name": user.name}
    result = conn.execute(users.insert().values(new_user))
    return conn.execute(users.select().where(users.c.user_id == result.lastrowid)).first()

# Editar un usuario
@user.put("/putUser/{id}")
def update_user(id: str, user: User):
    conn.execute(users.update().values(name = user.name).where(users.c.user_id == id))
    return conn.execute(users.select().where(users.c.user_id == id)).first()

# Eliminar usuario
@user.delete("/deleteUser/{id}")
def delete_user(id: str):
    conn.execute(users.delete().where(users.c.user_id == id))
    return Response(status_code=HTTP_204_NO_CONTENT)
# ======================================================================================

# ======================================RATING=========================================
# Obtener todos los ratings de tabla rating
@user.get("/getRatings")
def get_rating():
    return conn.execute(ratings.select()).fetchall()

# Agregar un rating
@user.post("/postRating")
def create_rating(rating: Rating):
    new_rating = {"user_id": rating.user_id,"book_id":rating.book_id,"rating": rating.rating}
    result = conn.execute(ratings.insert().values(new_rating))
    return 'Rating created'
# =======================================BOOK===========================================
# Obtener todos los libros de tabla Book
@user.get("/getBooks")
def get_books():
    return conn.execute(books.select()).fetchall()
# ======================================================================================

# ====================================BOOK_TAG===========================================
# Obtener todos los libros de tabla Book_tag
@user.get("/getBooksTag")
def get_books_tag():
    return conn.execute(books_tag.select()).fetchall()
# ======================================================================================

# =======================================TAG===========================================
# Obtener todos los libros de tabla Tags
@user.get("/getTags")
def get_tag():
    return conn.execute(tags.select()).fetchall()
# ======================================================================================