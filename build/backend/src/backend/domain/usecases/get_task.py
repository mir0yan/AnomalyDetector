from backend import interfaces
from backend.domain import entities
import logging


class GetTaskUsecase:

    def __init__(
            self,
            task_repository: interfaces.TaskRepository,
    ) -> None:
        self._task_repository = task_repository

    async def execute(self, task_id: str) -> entities.Task:
        msg_dbg = f"Getting task with id {task_id}."
        logging.debug(msg_dbg)

        task = await self._task_repository.get_task(task_id)

        msg_info = (
            f"Got task. ID: {task.id_}. "
        )
        logging.info(msg_info)

        return task
