from sqlmodel import create_engine, SQLModel, Session

from what_to_wear.api.utils.constants import DATABASE_URL
from what_to_wear.api.models.db_models.user import User  # noqa


engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
