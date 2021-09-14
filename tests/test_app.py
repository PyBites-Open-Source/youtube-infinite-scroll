import re

from fastapi.testclient import TestClient
import pytest
from requests.models import Response
from sqlmodel import Session, select

from youtube.db import insert_youtube_videos
from youtube.models import YouTube


def test_get_videos_from_channel_for_pybites(videos):
    assert len(videos) == 33
    video_ids = [vid["id"]["videoId"] for vid in videos]
    expected_ids = [
        "oDoFvpDftBA",
        "EbKeZkobGbA",
        "efqc3TkNAqk",
        "PiVOxEsr-Ag",
        "OWGyfBBwpSM",
        "zn6sdskawX0",
        "ejvql4eKev4",
        "B1kQIQx99Fw",
        "wqsn2ZPNo-U",
        "1GSNxPOuRL4",
        "MC2z2Xu7FME",
        "fPyQA7GnODo",
        "7ZQ9q7Cd9b0",
        "G-OAVLBFxbw",
        "WH6Gm0YKt54",
        "dsGwfjZxp9A",
        "_vfncxrKU54",
        "FwKA3eiwZnw",
        "Xc_O2n2UCO4",
        "V3-7RvipiSU",
        "5AQg2UxvXbI",
        "1QGEWBy6KTg",
        "Jpwn2yOppPo",
        "1OhKQsGz5hE",
        "2jeuMMU1a_o",
        "vJsyLSZxqVw",
        "O-Xsvbljj70",
        "Yx9qYl6lmzM",
        "9MYPvgz2Ob4",
        "Yk13k-_QZ-U",
        "xiGZhmBVfJM",
        "OD0Mc2GMMIA",
        "hvYID0shc3g",
    ]
    assert video_ids == expected_ids


def test_insert_youtube_videos(capfd, session: Session, videos):
    insert_youtube_videos(session, videos)
    output = capfd.readouterr()[0].strip()
    assert output == "Total records: 33 (newly inserted: 33)"
    # should not duplicate records
    insert_youtube_videos(session, videos)
    output = capfd.readouterr()[0].strip()
    assert output == "Total records: 33 (newly inserted: 0)"


def test_home_page_view(session: Session, client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

    video_ids = re.findall(
        r'href="https://youtu.be/(.*?)"', response.content.decode("utf-8")
    )

    statement = select(YouTube)
    results = session.exec(statement).all()
    first_video_ids_in_db = [yt.video_id for yt in results[:10]]

    expected_ids = [
        "oDoFvpDftBA",
        "EbKeZkobGbA",
        "efqc3TkNAqk",
        "PiVOxEsr-Ag",
        "OWGyfBBwpSM",
        "zn6sdskawX0",
        "ejvql4eKev4",
        "B1kQIQx99Fw",
        "wqsn2ZPNo-U",
        "1GSNxPOuRL4",
    ]
    assert video_ids == first_video_ids_in_db == expected_ids


def _parse_titles(response: Response) -> list[str]:
    return re.findall("<h2.*?>(.*?)</h2>", response.content.decode("utf-8"))


def test_read_more_videos(session: Session, client: TestClient, videos):
    response = client.get("/videos?offset=10&limit=10")
    html_result = _parse_titles(response)
    expected = [
        "11. Beating Imposter Syndrome as a Python Developer",
        "12. PyBites Developer Workshop",
        "13. PyBites Git Tricks Training",
        "14. PyBites Python Poetry Training",
        "15. PyBites Platform Introduction",
        "16. Use namedtuples for more readable code",
        "17. Comprehending Python comprehensions",
        "18. How to author a Bite exercise for the PyBites platform",
        "19. PyBites Code Challenges pytest functionality overview",
        "20. Generating Beautiful Code Snippets with Carbon and Selenium",
    ]
    assert html_result == expected
    response = client.get("/videos?offset=20&limit=10")
    html_result = _parse_titles(response)
    expected = [
        "21. Welcome to PyBites CodeChalleng.es!",
        "22. PyBites CodeChalleng.es Interview Bites Feature Demo",
        "23. Selenium Running on CodeChallenges",
        "24. Hacktoberfest: Submitting a PR to PyBites Code Challenges",
        "25. PyBites Code Challenge 51 (PCC 51) Overview",
        "26. Instructional: How to Fork and Submit a PR to our PyBites Code Challenges Repo",
        "27. Feature Overview: PyBites CodeChallenges Enterprise Tier Custom Bites",
        "28. Power to Pybites Slack Karmabot - Creating Commands",
        "29. New PyBites Certificates - how to earn, generate and upload them to LinkedIn",
        "30. Solving Python Bite Exercise 21. Query a nested data structure",
    ]
    assert html_result == expected
    response = client.get("/videos?offset=30&limit=10")
    html_result = _parse_titles(response)
    expected = [
        "31. CodeChalleng.es 100 Days of Python Tracking Grid",
        "32. Coding a Bite on CodeChalleng.es",
        "33. PyBites CodeChalleng.es New Dashboard Walkthrough 26-Mar-2018",
    ]
    assert html_result == expected
