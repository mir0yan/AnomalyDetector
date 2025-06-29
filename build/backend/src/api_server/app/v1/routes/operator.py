from fastapi import APIRouter, Path, Query, status

from api_server.app import dependency
from api_server.app.v1 import schema



operator_router = APIRouter(
    prefix="/api/v1/task",
    tags=["OPERATOR"],
)


@operator_router.post(
    "/create",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model": schema.response.create_task.CreateTaskResponseBody

        }
    },
)
async def create_task(  # noqa: ANN201
    body: schema.request.create_task.CreateTaskRequestBody,
):

    task_id = await dependency.create_task.execute(
        body.file_path
    )

    return schema.response.create_task.CreateTaskResponseBody.create(task_id)


@operator_router.get(
    "/{task_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "model":  schema.response.get_task.GetTaskResponseBody

        }
    },
)
async def create_task(  # noqa: ANN201
    task_id: str = Path(
        description="Identificator of the single search.",
        examples=["8b26f855-058d-4792-b5f0-72b11111da93"],
    ),
):
    task = await dependency.get_task.execute(
        task_id
    )

    return schema.response.get_task.GetTaskResponseBody.create(task)
