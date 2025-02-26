from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(unique=True)
    hashed_password: str = Field()
