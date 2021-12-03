from pydantic import BaseModel

# Schema de User donde se especifica cada tipo de dato
class Tag(BaseModel):
    tag_id: int
    tag_name: str