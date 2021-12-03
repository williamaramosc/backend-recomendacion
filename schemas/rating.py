from pydantic import BaseModel

# Schema de Rating donde se especifica cada tipo de dato
class Rating(BaseModel):
    user_id: int
    book_id: int
    rating: int