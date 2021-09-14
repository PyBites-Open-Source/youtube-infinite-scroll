from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
import pytest

from youtube.db import get_videos_from_channel
from youtube.main import app, get_session

PYBITES_YOUTUBE_CHANNEL = "UCBn-uKDGsRBfcB0lQeOB_gA"


@pytest.fixture(scope="session", name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="session", name="client")
def client_fixture(session: Session):
    """https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/"""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def vcr_config():
    return {"filter_query_parameters": ["key"]}


@pytest.fixture(scope="module")
@pytest.mark.vcr
def videos(vcr):
    # with vcr.use_cassette("tests/cassettes/videos.yaml"):
    return get_videos_from_channel(PYBITES_YOUTUBE_CHANNEL)
