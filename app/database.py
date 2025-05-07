from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# Credenciales en .env
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

# Validación individual de variables de entorno
if not all([MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE]):
    raise ValueError("Faltan credenciales en el archivo .env Asegúrate de definir: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE")

# Crear una instancia de motor para la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear una clase de sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base para la creación de modelos de datos
class Base(DeclarativeBase):
    pass

# Función para ejecutar el archivo .sql
def execute_sql_file(file_path):
    with engine.connect() as conn:
        with open(file_path, "r") as file:
            sql_script = file.read()
            # Dividir el script en consultas individuales
            statements = sql_script.split(";")
            for statement in statements:
                if statement.strip():  # Ignorar líneas vacías
                    conn.execute(text(statement))

# Ruta al archivo .sql
SQL_FILE_PATH = "app/sql/atenas.sql"

# Test de conexión
if __name__ == "__main__":
    try:
        # Intenta crear una sesión y cerrar la conexión
        execute_sql_file(SQL_FILE_PATH)
        print("Base de datos inicializada correctamente!")
        db = SessionLocal()
        print("Conexión exitosa a la base de datos!")
        db.close()
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        

