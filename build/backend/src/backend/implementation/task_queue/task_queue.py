import aio_pika
from backend.domain import entities
from backend import interfaces
from . import structures


class TaskQueueImpl(interfaces.TaskQueue):
    _PUBLISH_EXCHANGE_TYPE = aio_pika.ExchangeType.HEADERS
    _IS_PUBLISH_EXCHANGE_DURABLE = True

    def __init__(
            self,
            user: str,
            password: str,
            rabbit_ip: str,
            rabbit_port: int,
            tasks_exchange: str,
    ):
        self._user = user
        self._password = password
        self._rabbit_ip = rabbit_ip
        self._rabbit_port = rabbit_port
        self._tasks_exchange = tasks_exchange

        self._connection: aio_pika.abc.AbstractConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._task_exchange: aio_pika.abc.AbstractExchange | None = None
        self._queue: aio_pika.abc.AbstractQueue | None = None
        self._task_result_callback: interfaces.OnTaskResultCallback | None = None

    async def rpc_result_processor(
            self,
            on_task_result_callback: interfaces.OnTaskResultCallback
    ) -> None:
        self._task_result_callback = on_task_result_callback

        self._connection = await aio_pika.connect_robust(
            host=self._rabbit_ip,
            port=self._rabbit_port,
            login=self._user,
            password=self._password,
        )
        self._channel = await self._connection.channel(on_return_raises=True)
        self._task_exchange = await self._channel.declare_exchange(
            self._tasks_exchange,
            durable=True,
        )
        self._queue = await self._channel.declare_queue("amq.rabbitmq.reply-to")
        await self._queue.consume(
            callback=self._on_task_result_received,
            no_ack=True,
        )

    async def publish_task(self, task: entities.Task) -> None:

        message = self._build_message(task)

        await self._task_exchange.publish(message, routing_key="task.run")

    async def _on_task_result_received(self, message: aio_pika.abc.AbstractIncomingMessage) -> None:
        print("Got result")
        message_body = message.body.decode()
        task_id = message.correlation_id
        task_result = entities.Task.Result.model_validate_json(message_body)

        await self._task_result_callback(task_id, task_result)

    def _build_message(
            self,
            task: entities.Task,
    ) -> aio_pika.Message:
        task_params = structures.RabbitTask.from_entity(task)
        message_body = task_params.model_dump_json().encode()
        return aio_pika.Message(message_body, reply_to="amq.rabbitmq.reply-to", correlation_id=str(task.id_), )
