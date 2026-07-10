from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

# Construimos la URL de forma segura
url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)

print(url.render_as_string(hide_password=True))

try:
    engine = create_engine(url, echo=True)

    with engine.connect() as conn:
        print(conn.execute(text("SELECT version()")).scalar())

except Exception as e:
    import traceback
    traceback.print_exc()