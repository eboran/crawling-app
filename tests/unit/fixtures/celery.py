import pytest


@pytest.fixture
def mocked_city_task(mocker):
    return mocker.patch("src.celery.app.city_task.delay", return_value="All subtasks are created for this city")
