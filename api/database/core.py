from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite:///olist.db"

class NotFoundError(Exception):
    pass


class Base(DeclarativeBase):
    pass



class DBCustomers(Base):

    __tablename__ = "customers"

    customer_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    customer_unique_id: Mapped[str]
    customer_zip_code_prefix: Mapped[str] 
    customer_city: Mapped[str]
    customer_state: Mapped[str]



class DBUsers(Base):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True, index=True)
    email: Mapped[str]
    full_name: Mapped[str]
    disabled: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]

class DBToken(Base):

    __tablename__ = "tokens"

    username: Mapped[str] = mapped_column(primary_key=True, index=True)

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()
