from pydantic import BaseModel, StrictStr, StrictInt
from typing import Self
from enum import StrEnum, auto
from uuid import uuid4


class Status(StrEnum):
    IN_PROGRESS = auto()
    FINISHED = auto()


class Task(BaseModel):
    class Result(BaseModel):
        benign_thread: StrictInt
        attack_thread: StrictInt
    id_: StrictStr
    status: Status
    file_path: StrictStr
    result: Result | None

    @classmethod
    def new(cls, file_path: str) -> Self:
        return cls(
            id_=str(uuid4()),
            status=Status.IN_PROGRESS,
            file_path=file_path,
            result=None
        )

    def add_result(self, result: Result) -> None:
        self.result = result
        self.status = Status.FINISHED
