import abc
from backend.domain import entities
from .task_result_callback import OnTaskResultCallback


class TaskQueue(abc.ABC):

    @abc.abstractmethod
    async def publish_task(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def rpc_result_processor(
            self,
            on_task_result_callback: OnTaskResultCallback
    ) -> None:
        pass
