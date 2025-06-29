import aio_pika
from aio_pika import IncomingMessage, Exchange
from aio_pika.abc import AbstractIncomingMessage
from typing import Callable, Awaitable
import asyncio
import json
from ml_service.interfaces.task_queue_client import TaskQueueClient, OnTaskRecievedCallback
from ml_service.structures import Task

class RabbitTaskQueueClient(TaskQueueClient):
    def __init__(
        self,
        rabbit_url: str,
        exchange_name: str,
    ):
        self._rabbit_url = rabbit_url
        self._exchange_name = exchange_name
        self._connection: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._queue: aio_pika.abc.AbstractQueue | None = None

    async def rpc_call(self, on_task_recievedCallback: OnTaskRecievedCallback) -> None:
        self._connection = await aio_pika.connect_robust(self._rabbit_url)
        self._channel = await self._connection.channel()
        self._on_task_recievedCallback = on_task_recievedCallback
        # Подключение к существующей очереди (или создание)
        self._queue = await self._channel.declare_queue(
            name=self._exchange_name,
            durable=True,
            auto_delete=False,
        )
        await self._queue.bind(self._exchange_name, routing_key="task.run")

        # Подписка на сообщения
        await self._queue.consume(self._process_message, no_ack=False)


    async def _process_message(self, message: AbstractIncomingMessage):
        async with message.process():
            body = json.loads(message.body.decode())
            print(body)
            task = Task(
                task_id=body["task_id"],
                file_path=body["file_path"]
            )

        task_result = await self._on_task_recievedCallback(task)
        body = {
            "benign_thread": task_result.benign_thread,
            "attack_thread": task_result.attack_thread
        }
        response = aio_pika.Message(
            body=json.dumps(body).encode(),
            correlation_id=message.correlation_id,
        )

        default_exchange = Exchange(
            channel=message.channel,
            name="",
            type=aio_pika.ExchangeType.DIRECT,
            durable=True,
            internal=False,
            auto_delete=False,
        )
        await default_exchange.publish(
            response,
            routing_key=message.reply_to,
        )



