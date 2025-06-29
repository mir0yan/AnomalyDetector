from pydantic import BaseModel, StrictStr
from typing import Self
from backend.domain import entities


class RabbitTask(BaseModel):
    task_id: StrictStr
    file_path: StrictStr

    @classmethod
    def from_entity(cls, task: entities.Task) -> Self:
        return cls(
            task_id=task.id_,
            file_path=task.file_path
        )
