import abc
import pathlib
from ml_service.structures import TaskResult

class MLPredictor(abc.ABC):


    @abc.abstractmethod
    def predict_anomaly(self, csv_file: pathlib.Path) -> TaskResult:
        pass




