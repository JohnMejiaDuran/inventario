# db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Crear la carpeta data si no existe
if not os.path.exists('data'):
    os.makedirs('data')

# Configurar la base de datos
DATABASE_URL = "sqlite:///data/app.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()