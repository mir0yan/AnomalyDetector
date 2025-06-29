import asyncio
import pathlib
from concurrent.futures import ProcessPoolExecutor
import tempfile
from ml_service.interfaces import TaskQueueClient, MLPredictor, PcapConverter
from ml_service.structures import Task, TaskResult

class Manager:
    def __init__(
        self,
        task_queue_client: TaskQueueClient,
        pcap_converter: PcapConverter,
        ml_predictor: MLPredictor
    ):
        self._task_queue_client = task_queue_client
        self._ml_predictor = ml_predictor
        self._pcap_converter = pcap_converter

    async def start(self,) -> None:
        self._process_pool_executor = ProcessPoolExecutor()
        await self._task_queue_client.rpc_call(self._process_task)
        await asyncio.Future()

    async def _process_task(self, task: Task) -> TaskResult:

        with tempfile.TemporaryDirectory() as temp_dir:
            # convert_to_csv\
            loop = asyncio.get_running_loop()
            csv_file_path = await loop.run_in_executor(self._process_pool_executor, self._pcap_converter.convert_to_csv, pathlib.Path(task.file_path), pathlib.Path(temp_dir))
            # preprocess + predict
            return await loop.run_in_executor(self._process_pool_executor,self._ml_predictor.predict_anomaly, csv_file_path)



       