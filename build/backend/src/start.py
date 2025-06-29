import os
import pathlib
from dotenv import load_dotenv
import api_server
import logging
from utils import ConfigurationObtainer, UsecasesBuilder


env_path = pathlib.Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def main() -> int:
    try:
        config = ConfigurationObtainer.get_config()
    except Exception:
        msg_crit = "Error during configuration obtainment."
        logging.critical(msg_crit, exc_info=True)
        return 1

    try:
        usecases_builder = UsecasesBuilder(config)
        web_app = api_server.create_app(
            usecases_builder.build_create_task(),
            usecases_builder.build_get_task(),
            usecases_builder.build_add_task_result(),
            usecases_builder.build_task_result_updater_service()
        )
    except Exception:
        msg_crit = "Error during service's initialization. Check configs."
        logging.critical(msg_crit, exc_info=True)
        return 1

    try:
        api_server.start_api_server(
            web_app,
            host="0.0.0.0",
            port=int(os.environ["SERVE_PORT"]),
        )
    except Exception:
        msg_crit = "Critical error during service's work."
        logging.critical(msg_crit, exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit_code = main()

    os._exit(exit_code)
