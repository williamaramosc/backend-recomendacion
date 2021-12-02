import pandas as pd

import numpy as np

from typing import Optional

from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"items":{"item_id": item_id, "q": q}}