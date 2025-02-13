from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(unique=True)
    hashed_password: str = Field()
