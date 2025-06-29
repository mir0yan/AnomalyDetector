import asyncio
from utils import ConfigurationObtainer, Configuration

import os
import pathlib
from dotenv import load_dotenv
from ml_service import Manager
from ml_service.implementation import RabbitTaskQueueClient, CicFlowMeterPcapConverter, RandomForestMLPredictor
import logging


env_path = pathlib.Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

def main() -> int:
    try:
        config = ConfigurationObtainer.get_config()
    except Exception:
        msg_crit = "Error during configuration obtainment."
        logging.critical(msg_crit, exc_info=True)
        return 1

    rabbit_url = f"amqp://{config.queue_config.user}:{config.queue_config.password}@{config.queue_config.host}:{config.queue_config.port}/"
    
    rabbit_queue_client = RabbitTaskQueueClient(rabbit_url, config.queue_config.exchange_name)


    manager = Manager(
        rabbit_queue_client,
        CicFlowMeterPcapConverter(),
        RandomForestMLPredictor()
    )
    try:
        asyncio.run(manager.start())
    except Exception:
        msg_crit = "Critical error during service's work."
        logging.critical(msg_crit, exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()

    os._exit(exit_code)
