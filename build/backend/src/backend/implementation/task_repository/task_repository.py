import abc
from backend.domain import entities
from backend import interfaces
from redis.asyncio import Redis

from . import models


class TaskRepositoryImpl(interfaces.TaskRepository):

    def __init__(
            self,
            host: str,
            port: int,
            password: str,
    ) -> None:
        self._redis_client = Redis(host=host, port=port, password=password)

    async def add_task(self, task: entities.Task) -> None:
        task_model = models.TaskModel.from_entity(task)

        await self._add_items_to_hash(
            hash_name=task.id_,
            key_to_value=task_model.to_dict(),
        )

    async def get_task(self, task_id: str) -> entities.Task | None:
        async with self._redis_client.pipeline() as pipeline:
            pipeline.hgetall(task_id)

            pipeline_results = await pipeline.execute()

            raw_task = pipeline_results[0]

        if not raw_task:
            return None
        task_model = models.TaskModel.from_binary_dict(raw_task)

        return entities.Task(
            id_=task_model.id_,
            status=task_model.status,
            file_path=task_model.file_path,
            result=entities.Task.Result.model_validate_json(task_model.result) if task_model.result else None
        )

    async def update_task(self, task: entities.Task) -> None:
        await self.add_task(task)

    async def _add_items_to_hash(
            self, hash_name: str, key_to_value: dict[str, str]
    ) -> None:
        async with self._redis_client.pipeline() as pipeline:
            print(key_to_value)
            # pipeline.hset(hash_name, mapping=key_to_value)
            # old redis

            for k, v in key_to_value.items():
                pipeline.hset(hash_name, k, v)
            await pipeline.execute()
