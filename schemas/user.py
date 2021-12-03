from pydantic import BaseModel

# Schema de User donde se especifica cada tipo de dato
class User(BaseModel):
    user_id: int
    name: str