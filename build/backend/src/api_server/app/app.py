
from fastapi import FastAPI

from backend.domain import usecases

from . import dependency

from .v1 import routes as routes_v1

from . import lifespan

def create_app(
    create_task: usecases.CreateTaskUsecase,
    get_task: usecases.GetTaskUsecase,
    add_task_result: usecases.AddTaskResultUsecase,
    task_result_updater_service: usecases.TaskResultUpdaterServiceUsecase
) -> FastAPI:

    dependency.create_task = create_task
    dependency.get_task = get_task
    dependency.add_task_result = add_task_result
    dependency.task_result_updater_service = task_result_updater_service

    app = FastAPI(
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        lifespan=lifespan.lifespan
    )

    app.include_router(routes_v1.operator_router)

    return app
