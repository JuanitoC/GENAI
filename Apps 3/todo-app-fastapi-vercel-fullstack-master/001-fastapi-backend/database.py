# Importaciones necesarias para la configuración de la base de datos
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# URL de conexión comentada (versión anterior)
#SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}"

# Obtención de las credenciales de la base de datos desde variables de entorno
user = os.environ['DATABASE_USER']        # Usuario de la base de datos
password = os.environ['DATABASE_PASSWORD'] # Contraseña de la base de datos
host = os.environ['DATABASE_HOST']        # Host de la base de datos
port = os.environ['DATABASE_PORT']        # Puerto de la base de datos
db_name = os.environ['DATABASE_NAME']     # Nombre de la base de datos

# Construcción de la URL de conexión a PostgreSQL
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_base_datos
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

# Creación del motor de base de datos
# El motor es responsable de manejar la conexión a la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Creación de la fábrica de sesiones
# SessionLocal se usa para crear sesiones de base de datos
# autocommit=False: Los cambios no se guardan automáticamente
# autoflush=False: No se ejecutan consultas automáticamente
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creación de la clase base para los modelos
# Base es la clase padre de la que heredan todos los modelos de SQLAlchemy
Base = declarative_base()