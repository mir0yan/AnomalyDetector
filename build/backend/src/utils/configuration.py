import abc

from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr
import os


class Configuration(BaseModel):
    class Repository(BaseModel):
        host: StrictStr
        port: StrictInt
        password: StrictStr

    class Queue(BaseModel):
        host: StrictStr
        port: StrictInt
        user: StrictStr
        password: StrictStr
        exchange_name: StrictStr

    repository_config: Repository
    queue_config: Queue


class ConfigurationObtainer:
    @classmethod
    def get_config(cls,) -> Configuration:
        return Configuration(
            repository_config=Configuration.Repository(
                host=os.environ["REPO_HOST"],
                port=int(os.environ["REPO_PORT"]),
                password=os.environ["REPO_PASS"]
            ),
            queue_config=Configuration.Queue(
                host=os.environ["QUEUE_HOST"],
                port=int(os.environ["QUEUE_PORT"]),
                user=os.environ["QUEUE_USER"],
                password=os.environ["QUEUE_PASS"],
                exchange_name=os.environ["QUEUE_EXCHANGE"]
            )
        )
