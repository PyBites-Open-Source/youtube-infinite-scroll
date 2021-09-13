from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class YouTube(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    video_id: str
    title: str
    description: str
    thumb: str
    published: datetime


class YouTubeRead(SQLModel):
    id: int
    video_id: str
    title: str
    description: str
    thumb: str
    published: datetime
