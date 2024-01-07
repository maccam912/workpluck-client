import httpx
import time
from typing import Optional

from workpluck_client.models import (
    ResultRetrievalResponse,
    ResultSubmission,
    TaskRetrievalResponse,
    TaskSubmission,
    TaskSubmissionResponse,
)


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client()

    # Synchronous methods
    def get_task(self, topic: str) -> Optional[TaskRetrievalResponse]:
        response = self.client.get(f"{self.base_url}/task", params={"topic": topic})
        if response.status_code == 200:
            return TaskRetrievalResponse(**response.json())
        return None

    def post_result(self, task_id: str, result: dict):
        data = ResultSubmission(id=task_id, output=result)
        self.client.post(f"{self.base_url}/result", json=data.model_dump())

    def submit_task(self, topic: str, input_data: dict) -> str:
        data = TaskSubmission(topic=topic, input=input_data)
        response = self.client.post(f"{self.base_url}/task", json=data.dict())
        result = TaskSubmissionResponse(**response.json())
        return result.id

    def get_result(self, task_id: str) -> Optional[dict]:
        response = self.client.get(
            f"{self.base_url}/result", params={"id": task_id}
        )
        if response.status_code == 200:
            return ResultRetrievalResponse(**response.json()).output
        return None

    # Asynchronous methods
    async def async_get_task(self, topic: str) -> Optional[TaskRetrievalResponse]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/task", params={"topic": topic}
            )
            if response.status_code == 200:
                return TaskRetrievalResponse(**response.json())
            return None

    async def async_post_result(self, task_id: str, result: dict):
        data = ResultSubmission(id=task_id, output=result)
        async with httpx.AsyncClient() as client:
            await client.post(f"{self.base_url}/result", json=data.model_dump())

    async def async_submit_task(self, topic: str, input_data: dict) -> str:
        data = TaskSubmission(topic=topic, input=input_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/task", json=data.model_dump())
            result = TaskSubmissionResponse(**response.json())
            return result.id

    async def async_get_result(self, task_id: str) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/result", params={"id": task_id}
            )
            if response.status_code == 200:
                return ResultRetrievalResponse(**response.json()).output
            return None

    # Convenience method
    def call(self, topic: str, input_data: dict) -> Optional[dict]:
        task_id = self.submit_task(topic, input_data)
        while True:
            result = self.get_result(task_id)
            if result is not None:
                return result
            time.sleep(1)  # Polling interval
