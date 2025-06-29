import abc
import pathlib


class PcapConverter(abc.ABC):


    @abc.abstractmethod
    def convert_to_csv(self, pcap_file_path: pathlib.Path, destination_folder_path: pathlib.Path) -> pathlib.Path:
        pass




