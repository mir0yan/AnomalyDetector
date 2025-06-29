from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr
import os


class Configuration(BaseModel):

    class Queue(BaseModel):
        host: StrictStr
        port: StrictInt
        user: StrictStr
        password: StrictStr
        exchange_name: StrictStr

    queue_config: Queue


class ConfigurationObtainer:
    @classmethod
    def get_config(cls,) -> Configuration:
        return Configuration(
            queue_config=Configuration.Queue(
                host=os.environ["QUEUE_HOST"],
                port=int(os.environ["QUEUE_PORT"]),
                user=os.environ["QUEUE_USER"],
                password=os.environ["QUEUE_PASS"],
                exchange_name=os.environ["QUEUE_EXCHANGE"]
            )
        )
