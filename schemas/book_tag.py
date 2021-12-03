from pydantic import BaseModel

# Schema de book_tag donde se especifica cada tipo de dato
class Book_Tag(BaseModel):
    goodreads_book_id: int
    tag_id: int
    count: int