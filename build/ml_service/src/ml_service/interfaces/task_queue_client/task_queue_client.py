import abc

from .on_task_recieved_callback import OnTaskRecievedCallback

class TaskQueueClient(abc.ABC):


    @abc.abstractmethod
    async def rpc_call(self, on_task_recievedCallback: OnTaskRecievedCallback) -> None:
        pass




