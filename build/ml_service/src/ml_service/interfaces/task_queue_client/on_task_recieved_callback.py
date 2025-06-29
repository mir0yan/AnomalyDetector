from pydantic import BaseModel, StrictStr

import typing as t
from ml_service import Task, TaskResult


OnTaskRecievedCallback: t.TypeAlias =  t.Callable[[Task], t.Coroutine[t.Any, t.Any, t.Any]]
