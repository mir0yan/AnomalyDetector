from pydantic import BaseModel


class SuccessResponse(BaseModel):
    result: BaseModel | dict
