from typing import Self

from pydantic import BaseModel, Field, StrictInt, StrictStr


from . import base


class CreateTaskResponseBody(base.SuccessResponse):
    class CreateTaskResult(BaseModel):
        task_id: StrictStr = Field(
            description="Identificator of the search. UUID4 format.",
            examples=["8b26f855-058d-4792-b5f0-72b11111da93"],
        )

    result: CreateTaskResult

    @classmethod
    def create(cls, id_: str) -> Self:
        print(id_)
        return cls(result=CreateTaskResponseBody.CreateTaskResult(task_id=id_))
