from sqlalchemy import create_engine, MetaData

# Datos de conexion para la base de datos
DATABASE_URL = "mysql+pymysql://root123:root123@35.238.124.195:3306/baserecomendacion"
engine = create_engine(DATABASE_URL)

meta = MetaData()
conn = engine.connect()

