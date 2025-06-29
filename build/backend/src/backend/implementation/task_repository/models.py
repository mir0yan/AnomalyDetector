import json
from typing import Self

from pydantic import BaseModel, StrictStr

from backend.domain import entities


class TaskModel(BaseModel):
    id_: StrictStr
    status: str
    file_path: StrictStr
    result: str | None

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_binary_dict(cls, raw_search: dict[bytes, bytes]) -> Self:
        return cls(**{key.decode("utf-8"): value.decode("utf-8") for key, value in raw_search.items()})

    @classmethod
    def from_entity(cls, task: entities.Task) -> Self:
        return cls(
            id_=task.id_,
            status=str(task.status),
            file_path=str(task.file_path),
            result=task.result.model_dump_json() if task.result else "",
        )
