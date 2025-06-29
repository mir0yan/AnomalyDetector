from backend import interfaces
from backend.domain import usecases
import logging


class TaskResultUpdaterServiceUsecase:

    def __init__(
            self,
            task_queue: interfaces.TaskQueue,
            add_task_result: usecases.AddTaskResultUsecase
    ) -> None:
        self._task_queue = task_queue
        self._add_task_result = add_task_result

    async def start(self) -> None:
        msg_info = f"Awaiting tasks result."
        logging.info(msg_info)

        await self._task_queue.rpc_result_processor(self._add_task_result.execute)

        msg_info = (
            f"Finishing awaiting for tasks."
        )
        logging.info(msg_info)
