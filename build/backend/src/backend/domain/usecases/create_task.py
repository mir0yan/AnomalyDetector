from backend import interfaces
from backend.domain import entities
import logging


class CreateTaskUsecase:

    def __init__(
            self,
            task_queue: interfaces.TaskQueue,
            task_repository: interfaces.TaskRepository,
    ) -> None:
        self._task_queue = task_queue
        self._task_repository = task_repository

    async def execute(self, file_path: str) -> str:
        msg_dbg = f"Creating task. FILE_PATH: {file_path}."
        logging.debug(msg_dbg)

        task = entities.Task.new(
            file_path=file_path
        )

        await self._task_repository.add_task(task)

        await self._task_queue.publish_task(task)

        msg_info = (
            f"New task is created. ID: {task.id_}. "
        )
        logging.info(msg_info)

        return task.id_
