import logging
import requests
import uuid
from pixegami.custom_logger import customLogger


class ToDoApi():
    ENDPOINT = "https://todo.pixegami.io"
    log = customLogger(logging.DEBUG)

    def create_task(self, payload):
        self.log.info(f"Sending PUT request to create a new task with payload: {payload}")
        return requests.put(self.ENDPOINT + "/create-task", json=payload)

    def get_task(self, task_id):
        self.log.info(f"Sending GET request to get an existing task: {task_id}")
        return requests.get(self.ENDPOINT + f"/get-task/{task_id}")

    def new_task_payload(self):
        user_id = f"test_user_{uuid.uuid4().hex}"
        content = f"test_content_{uuid.uuid4().hex}"
        self.log.info(f"Creating task for user {user_id} with content {content}")

        return {
            "content": content,
            "user_id": user_id,
            "is_done": False,
        }

    def update_task(self, payload):
        self.log.info(f"Sending PUT request to update an existing task with payload: {payload}")
        return requests.put(self.ENDPOINT + "/update-task", json=payload)

    def list_task(self, user_id):
        self.log.info(f"Sending GET request to list existing task for user: {user_id}")
        return requests.get(self.ENDPOINT + f"/list-tasks/{user_id}")

    def delete_task(self, task_id):
        self.log.info(f"Sending GET request to delete task: {task_id}")
        return requests.get(self.ENDPOINT + f"/delete-task/{task_id}")