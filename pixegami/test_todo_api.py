'''
HTTP Response Status Codes
1. Informational responses (100-199)
2. Successful responses (200-299)
3. Redirection messages (300-399)
4. Client error responses (400-499)
5. Server error responses (500-599)
'''
import logging, pytest
from pixegami.to_do_api import ToDoApi
from pixegami.custom_logger import customLogger



class TestTodoApi():
    logger = customLogger(logLevel=logging.DEBUG)
    api_helper = ToDoApi()

    @pytest.mark.tcid1
    def test_can_create_task(self):
        payload = self.api_helper.new_task_payload()
        create_task_response = self.api_helper.create_task(payload)
        assert create_task_response.status_code == 200

        data = create_task_response.json()
        print(data)

        task_id = data["task"]["task_id"]
        get_task_response = self.api_helper.get_task(task_id)

        assert get_task_response.status_code == 200
        get_task_data = get_task_response.json()
        self.logger.info(get_task_data)
        assert get_task_data["content"] == payload["content"]
        assert get_task_data["user_id"] == payload["user_id"]

    @pytest.mark.tcid2
    def test_can_update_task(self):
        # create a task
        payload = self.api_helper.new_task_payload()
        create_task_response = self.api_helper.create_task(payload)
        assert create_task_response.status_code == 200
        task_id = create_task_response.json()["task"]["task_id"]
        user_id = create_task_response.json()["task"]["user_id"]
        self.logger.info(f"user_id: {user_id} | task_id: {task_id}")

        # update the task
        new_payload = {
            "user_id": user_id,
            "task_id": task_id,
            "content": "my updated content",
            "is_done": True,
        }
        self.logger.info(new_payload)
        update_task_response = self.api_helper.update_task(new_payload)
        self.logger.info(f"Update task response: {update_task_response.status_code}")
        assert update_task_response.status_code == 200

        # get and validate the changes
        get_task_response = self.api_helper.get_task(task_id)
        self.logger.info(f"get_task_response: {get_task_response.status_code}")
        assert get_task_response.status_code == 200

        get_task_data = get_task_response.json()
        self.logger.info(f"get_task_data: {get_task_data}")
        self.logger.info(f'get_task_data content: {get_task_data["content"]} '
                         f'-- new payload content: {new_payload["content"]}')
        assert get_task_data["content"] == new_payload["content"]
        assert get_task_data["is_done"] == new_payload["is_done"]

    @pytest.mark.tcid3
    def test_can_list_tasks(self):
        # create N tasks
        n = 3
        payload = self.api_helper.new_task_payload()

        for _ in range(n):
            create_task_response = self.api_helper.create_task(payload)
            assert create_task_response.status_code == 200

        # Lists tasks and check that there are N items
        user_id = payload["user_id"]
        list_task_response = self.api_helper.list_task(user_id)
        assert list_task_response.status_code == 200
        data = list_task_response.json()
        self.logger.info(data)

        tasks = data["tasks"]
        assert len(tasks) == n

    @pytest.mark.tcid4
    def test_can_delete_task(self):
        # create task
        payload = self.api_helper.new_task_payload()
        create_task_response = self.api_helper.create_task(payload)
        assert create_task_response.status_code == 200

        # get task id
        task_id = create_task_response.json()["task"]["task_id"]

        # delete task
        delete_task_response = self.api_helper.delete_task(task_id)
        assert delete_task_response.status_code == 200

        # try to fetch deleted task and assert
        get_task_response = self.api_helper.get_task(task_id)
        assert get_task_response.status_code == 404



