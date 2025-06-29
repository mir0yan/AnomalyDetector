from backend.domain import entities, usecases
from backend.implementation import TaskRepositoryImpl, TaskQueueImpl


from .configuration import Configuration


class UsecasesBuilder:
    def __init__(self, config: Configuration) -> None:
        self._config = config

        self._task_queue = TaskQueueImpl(
            self._config.queue_config.user,
            self._config.queue_config.password,
            self._config.queue_config.host,
            self._config.queue_config.port,
            self._config.queue_config.exchange_name
        )

        self._task_repo = TaskRepositoryImpl(
            self._config.repository_config.host,
            self._config.repository_config.port,
            self._config.repository_config.password
        )

    def build_create_task(self) -> usecases.CreateTaskUsecase:
        return usecases.CreateTaskUsecase(self._task_queue, self._task_repo)

    def build_get_task(self) -> usecases.GetTaskUsecase:
        return usecases.GetTaskUsecase(self._task_repo)

    def build_add_task_result(self) -> usecases.AddTaskResultUsecase:
        return usecases.AddTaskResultUsecase(self._task_repo)

    def build_task_result_updater_service(self) -> usecases.TaskResultUpdaterServiceUsecase:
        return usecases.TaskResultUpdaterServiceUsecase(self._task_queue, self.build_add_task_result())
