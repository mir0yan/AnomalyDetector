from typing import Self

from pydantic import BaseModel, Field, StrictInt, StrictStr
from backend.domain import entities

from . import base


class GetTaskResponseBody(base.SuccessResponse):
    class GetTaskResult(BaseModel):
        class TaskResult(BaseModel):
            benign_threads: StrictInt
            attack_threads: StrictInt
        task_id: StrictStr = Field(
            description="Identificator of the task. UUID4 format.",
            examples=["8b26f855-058d-4792-b5f0-72b11111da93"],
        )
        status: StrictStr = Field(
            description="Status of task.",
            examples=["IN_PROGRESS", "FINISHED"],
        )
        result: TaskResult | None

    result: GetTaskResult

    @classmethod
    def create(cls, task: entities.Task) -> Self:
        return cls(
            result=GetTaskResponseBody.GetTaskResult(
                task_id=task.id_,
                status=task.status,
                result=GetTaskResponseBody.GetTaskResult.TaskResult(
                    benign_threads=task.result.benign_thread,
                    attack_threads=task.result.attack_thread,
                ) if task.result else None
            )
        )
