from fastapi import Depends, FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlmodel import select, Session

from youtube.models import YouTube
from youtube.db import get_session

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DOMAIN = "http://localhost:8000"
YOUTUBE_BASE_URL = "https://youtu.be/"
TR_CONTENT = """
<tr hx-get='{domain}/videos/?offset={offset}&limit={limit}' hx-trigger='revealed' hx-swap='afterend'>
"""
TR_INNER_HTML = """
<td>
  <h2 class="mui--text-subhead">{idx}. {title}</h2>
  <p>{description} (published: {published})</p>
</td>
<td>
  <a href="{link}" target="_blank">
    <img src="{thumb}" alt="play this video">
  </a>
</td>
"""


def _get_video_content(videos: list[YouTube]) -> list[str]:
    content = []
    for video in videos:
        content.append(
            TR_INNER_HTML.format(
                idx=video.id,
                title=video.title,
                description=video.description,
                published=video.published,
                link=YOUTUBE_BASE_URL + video.video_id,
                thumb=video.thumb,
            )
        )
    return content


@app.get("/", response_class=HTMLResponse)
def home(*, session: Session = Depends(get_session), request: Request):
    videos = session.exec(select(YouTube).offset(0).limit(10)).all()
    content = _get_video_content(videos)
    tr_with_next_row_get = TR_CONTENT.format(domain=DOMAIN, offset=10, limit=10).strip()
    context = {
        "request": request,
        "content": content,
        "tr_with_next_row_get": tr_with_next_row_get,
    }
    return templates.TemplateResponse("index.html", context)


@app.get("/videos/")
def read_videos(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    content = ""
    videos = session.exec(select(YouTube).offset(offset).limit(limit)).all()
    if videos:
        content = [f"<tr>{tds}</tr>" for tds in _get_video_content(videos)]
        # give the last tr element the htmx to enable infinite scroll
        content[-1] = content[-1].replace(
            "<tr>", TR_CONTENT.format(domain=DOMAIN, offset=offset + limit, limit=limit)
        )
        content = "\n".join(content)

    return HTMLResponse(content=content, status_code=200)
