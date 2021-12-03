import pandas as pd

import numpy as np

from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel

from routes.routes import user

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import linear_kernel

from scipy.stats import pearsonr

import mysql.connector

from sqlalchemy import create_engine

import json

DATABASE_URL = "mysql+mysqlconnector://root123:root123@35.238.124.195:3306/baserecomendacion"

engine = create_engine(DATABASE_URL, echo=False)

sql = "select * from users where user_id = 60000"
usuario = pd.read_sql(sql, DATABASE_URL)

print(usuario.empty)