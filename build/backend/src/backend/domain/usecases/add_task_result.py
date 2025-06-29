from backend import interfaces
from backend.domain import entities
import logging


class AddTaskResultUsecase:

    def __init__(
            self,
            task_repository: interfaces.TaskRepository,
    ) -> None:
        self._task_repository = task_repository

    async def execute(self, task_id: str, result: entities.Task.Result) -> entities.Task:
        msg_dbg = f"Updating task with id {task_id}."
        logging.debug(msg_dbg)

        task = await self._task_repository.get_task(task_id)

        task.add_result(
            result
        )

        await self._task_repository.update_task(task)

        msg_info = (
            f"Updated task. ID: {task.id_}. "
        )
        logging.info(msg_info)

        return task
