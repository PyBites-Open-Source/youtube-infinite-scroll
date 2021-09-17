# YouTube infinite scroll

This demo uses [SQLModel](https://sqlmodel.tiangolo.com/) and [htmx](https://htmx.org/) to generate an [infinite scroll](https://htmx.org/examples/infinite-scroll/) of videos of a YouTube videos.

## Setup

Make a virtual environment and install the requirements:

```
$ make install
python3.9 -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt
```

Then go to [Google Cloud Platform > YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com?project=top-repos) and hit the blue ENABLE button, then generate your API key:

![enable the API](assets/youtube-api1.png)

![create an API key](assets/youtube-api2.png)

Next set up your `.env` file:

```
cp .env-example .env
```

Populate it with the following environment variables:

- `YT_CHANNEL`: the YouTube channel to use this on, to try it out with PyBites you can use `UCBn-uKDGsRBfcB0lQeOB_gA` or for PyCon use `UCMjMBMGt0WJQLeluw6qNJuA` (demo below).

- `YOUTUBE_API_KEY`: the API key you just created.

- `DATABASE_URL`: create a database and point to it (in case of `sqlite` all you need to do is specify one like this: `sqlite:///db.sqlite3`)

Next let's cache the YouTube channel's data (all videos' metadata) to not exhaust the YouTube API rate limit.

Run the following command with your virtual environment enabled (this example uses PyCon's YouTube channel):

```
$ make dbsetup
source venv/bin/activate && python -m youtube.db
Total records: 172 (newly inserted: 172)
```

Result:

<video src="https://user-images.githubusercontent.com/387927/133118592-87d5b8d3-a87c-4be3-81f1-8457c0eb182c.mp4" controls="controls" style="max-width: 730px;">
</video>

Lastly run the app:

```
make run
```

Navigate to [localhost:8000](http://localhost:8000/) and you should see something like this:

<video src="https://user-images.githubusercontent.com/387927/133118934-29655671-8d4e-4483-8a3e-cdffe0fabbd4.mp4" controls="controls" style="max-width: 730px;">
</video>

## Testing

There are unit and functional tests for this project.

The unit tests use "cassettes" (cached API responses) so they are fast:

<video src="https://www.dropbox.com/s/763t4zjfzbjfqn9/yi-infinite-scroll-unit-test.mp4?dl=0" controls="controls" style="max-width: 730px;">
</video>

The functional (end-to-end) test uses the real DB that is configured in `.env` and Selenium to scroll to the bottom of the infinite scroll, then compare the amount of table rows on the page vs the amount of entries in the DB. This test requires FastAPI to be running.

So in terminal 1 run:

```
make run
```

Then in terminal 2 run the test:

<video src="https://www.dropbox.com/sh/x9al60o8nl5mx8x/AABKKXnJyW1FwTbHG6tAWZDwa?dl=0" controls="controls" style="max-width: 730px;">
</video>

Of course you can also run all tests in one go with `make test`.
