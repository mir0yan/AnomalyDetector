import typing as t
from backend.domain import entities


OnTaskResultCallback: t.TypeAlias = t.Callable[[str, entities.Task.Result], t.Coroutine[t.Any, t.Any, t.Any]]
