from pydantic import BaseModel

# Schema de Rating donde se especifica cada tipo de dato
class Book(BaseModel):
    book_id: int
    goodreads_book_id: int
    authors: str
    original_publication_year: int
    title: str
    average_rating: float
    ratings_count: int
    language_code: str
    image_url: str