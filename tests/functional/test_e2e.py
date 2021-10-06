from collections import deque
from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from sqlmodel import Session, select

from youtube.db import engine
from youtube.models import YouTube


@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    try:
        driver.get("http://localhost:8000/")
        yield driver
    except WebDriverException:
        raise RuntimeError("Cannot get to localhost:8000, did you start FastAPI?")
    finally:
        driver.quit()


@pytest.fixture(scope="session")
def scroll_to_end(driver):
    cache_size = 5
    num_rows = deque(maxlen=cache_size)
    i = 0

    while True:
        last_element = driver.find_elements_by_class_name("mui--text-subhead")[-1]
        actions = webdriver.ActionChains(driver)
        actions.move_to_element(last_element).perform()
        i += 1

        num_rows.append(len(driver.find_elements_by_tag_name("tr")))

        if i > cache_size and num_rows.count(num_rows[-1]) == len(num_rows):
            print("num rows stable, seems I hit the end of infinite scroll")
            break


def test_number_of_rows_on_page(session, driver, scroll_to_end):
    with Session(engine) as session:
        num_row_in_db_table = len(session.exec(select(YouTube)).all())
    num_rows_on_page = len(driver.find_elements_by_tag_name("tbody tr"))
    assert num_rows_on_page == num_row_in_db_table
