from datetime import datetime
from typing import Optional
import os

from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, create_engine

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


class YouTube(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: str
    title: str
    description: str
    thumb: str
    published: datetime


engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
