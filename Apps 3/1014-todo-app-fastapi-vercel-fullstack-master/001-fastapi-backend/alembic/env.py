# Importaciones necesarias para Alembic
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Este es el objeto de configuración de Alembic
# Proporciona acceso a los valores dentro del archivo .ini en uso
config = context.config

# Configuración comentada de la URL de la base de datos (versión anterior)
#config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")

# Configuración de la URL de conexión a PostgreSQL para Alembic
# Construye la URL usando las variables de entorno
config.set_main_option("sqlalchemy.url", f"postgresql://{os.environ['DATABASE_USER']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}:{os.environ['DATABASE_PORT']}/{os.environ['DATABASE_NAME']}")


# Interpreta el archivo de configuración para el logging de Python
# Esta línea configura los loggers básicamente
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Agrega aquí el objeto MetaData de tu modelo
# para soporte de 'autogenerate'
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# otros valores de la configuración, definidos por las necesidades de env.py,
# pueden ser adquiridos:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """
    Ejecuta migraciones en modo 'offline'.
    
    Esto configura el contexto con solo una URL
    y no un Engine, aunque un Engine es aceptable
    aquí también. Al omitir la creación del Engine
    ni siquiera necesitamos que un DBAPI esté disponible.
    
    Las llamadas a context.execute() aquí emiten la cadena dada
    a la salida del script.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecuta migraciones en modo 'online'.
    
    En este escenario necesitamos crear un Engine
    y asociar una conexión con el contexto.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Ejecuta las migraciones según el modo (offline u online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
