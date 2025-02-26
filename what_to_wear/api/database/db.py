from sqlmodel import Session, SQLModel, create_engine

from what_to_wear.api.models.db_models.user import User  # noqa
from what_to_wear.api.utils.constants import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
