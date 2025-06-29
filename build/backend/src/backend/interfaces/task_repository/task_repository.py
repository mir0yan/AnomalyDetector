import abc
from backend.domain import entities


class TaskRepository(abc.ABC):

    @abc.abstractmethod
    async def add_task(self, task: entities.Task) -> None:
        pass

    @abc.abstractmethod
    async def get_task(self, task_id: str) -> entities.Task:
        pass

    @abc.abstractmethod
    async def update_task(self, task: entities.Task) -> None:
        pass
