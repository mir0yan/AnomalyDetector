import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

import logging

from api_server.app import dependency

__background_tasks = set()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    await dependency.task_result_updater_service.start()
    yield
