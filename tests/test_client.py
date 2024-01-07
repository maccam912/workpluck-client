import pytest
from workpluck_client.client import Client, TaskRetrievalResponse, ResultRetrievalResponse

@pytest.fixture(scope='session')
def httpserver_listen_address():
    return ("127.0.0.1", 8080)

def test_submit_task(httpserver):
    task_id = "0e6d41c2-0269-4466-b1aa-10ed25eee4d6"
    httpserver.expect_request("/task").respond_with_json({"id": task_id}, status=201)

    client = Client(httpserver.url_for("/"))
    response_task_id = client.submit_task("example_topic", {"key": "value"})

    assert str(response_task_id) == task_id

def test_get_task(httpserver):
    task_id = "0e6d41c2-0269-4466-b1aa-10ed25eee4d6"
    httpserver.expect_request("/task").respond_with_json({"id": task_id, "input": {"key": "value"}}, status=200)

    client = Client(httpserver.url_for("/"))
    task = client.get_task("example_topic")

    assert task == TaskRetrievalResponse(id=task_id, input={"key": "value"})

# Similar tests can be written for post_result and get_result
