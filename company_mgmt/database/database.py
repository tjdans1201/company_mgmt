from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import sys

sys.dont_write_bytecode = True

url_format = "postgresql://{id}:{pw}@{host}:{port}/{db}"

# DATABASE_URL = url_format.format(
#     **{
#         "id": os.environ["DB_USER"],
#         "pw": os.environ["DB_PASS"],
#         "host": os.environ["DB_HOST"],
#         "port": os.environ["DB_PORT"],
#         "db": os.environ["DB_SCHEMA"],
#     }
# )

DATABASE_URL = url_format.format(
    **{
        "id": "postgres",
        "pw": "password",
        "host": "localhost",
        "port": "5432",
        "db": "wanted_db",
    }
)


engine = create_engine(
    DATABASE_URL,
    connect_args={"connect_timeout": 10},
    poolclass=NullPool,
    echo=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    데이터베이스 세션 취득
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()