import subprocess
import pathlib
from ml_service.interfaces import PcapConverter
import logging



class CicFlowMeterPcapConverter(PcapConverter):

    def convert_to_csv(
        self, pcap_file_path: pathlib.Path, destination_folder_path: pathlib.Path
    ) -> pathlib.Path:
        # convert_to_csv
        jnetpcap_path =  str(pathlib.Path(__file__).parent.absolute().resolve() / "source" / "jnetpcap-1.4.r1425").replace("\\", "\\\\")
        jar_path = str(pathlib.Path(__file__).parent.absolute().resolve() / "source" / "libs" / "CICFlowMeter-4.0-all.jar").replace("\\", "\\\\")

        target_class_name = "cic.cs.unb.ca.ifm.Cmd"
        cmd = (
            ["java"]
            + [f"-Djava.library.path={jnetpcap_path}"]
            + ["-cp", jar_path, target_class_name, str(pcap_file_path.absolute().resolve()), str(destination_folder_path.absolute().resolve())]
        )

        res = subprocess.run(cmd, capture_output=True, text=True)
        import sys
        if res.stdout:
            msg_dbg = f"=== Java stdout ===\n { res.stdout}"
            logging.error(msg_dbg)
        if res.stderr:
             msg_dbg = f"=== Java stderr ===\n { res.stderr}"
             logging.error(msg_dbg)
           


        converted_csv_path = pathlib.Path(destination_folder_path / f"{str(pcap_file_path.name)[:-4]}pcap_Flow.csv" )
        msg_dbg = f"Converted pcap to csv. Path: {converted_csv_path}"
        logging.info(msg_dbg)

        return converted_csv_path
