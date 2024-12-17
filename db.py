from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from db_model import Base, Pizza
from pizzas import pizzas

DB_URL = "sqlite:///./app_db.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


event.listen(engine, 'connect', _fk_pragma_on_connect)


def add_pizzas(target, connection, **kw):
    connection.execute(target.insert(), pizzas)


event.listen(Pizza.__table__, "after_create", add_pizzas)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
