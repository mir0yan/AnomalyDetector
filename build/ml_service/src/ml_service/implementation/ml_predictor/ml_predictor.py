import pathlib
import pandas as pd
import os
from sklearn import preprocessing
import numpy as np
import joblib
import string
import tempfile
from ml_service.structures import TaskResult
from ml_service.interfaces import MLPredictor

class RandomForestMLPredictor(MLPredictor):
    _LABELS = ["Bwd Packet Length Std", "Flow Bytes/s", "Total Length of Fwd Packets", "Fwd Packet Length Std",
     "Flow IAT Std", "Flow IAT Min", "Fwd IAT Total", "Timestamp"]

    def predict_anomaly(self, csv_file: pathlib.Path) -> TaskResult:
        preprocessed_csv = self._preprocess_csv(csv_file)
        return self._predict(preprocessed_csv)

    def _preprocess_csv(self, csv_file: pathlib.Path) -> pathlib.Path:
        main_labels =  ",".join(self._LABELS) + "\n"
        df = pd.read_csv(csv_file)

        # 2) Убираем колонку Label (она называется именно так)
        if "Label" in df.columns:
            df = df.drop(columns=["Label"])
        df.to_csv(csv_file, index=False)

        with tempfile.TemporaryFile("w+", delete=False) as temp_file:
            temp_file.write(main_labels)

            with open(csv_file, 'r', ) as in_csv_file:
                while True:
                    try:
                        line=in_csv_file.readline()
                        if  line[0] in string.digits:# this line eliminates the headers of CSV files and incomplete streams .
                            
                            if " – " in str(line): ##  if there is "–" character ("–", Unicode code:8211) in the flow ,  it will be chanced with "-" character ( Unicode code:45).
                                line=(str(line).replace(" – "," - "))
                            line=(str(line).replace("inf","0"))
                            line=(str(line).replace("Infinity","0"))
                            
                            line=(str(line).replace("NaN","0"))
                                
                            temp_file.write(str(line))
                        else:
                            continue                       
                    except:
                        break
            temp_file.flush()
            temp_file.seek(0)
            df=pd.read_csv(temp_file, low_memory=False)
            df=df.fillna(0)

        os.unlink(temp_file.name)

        # process flow bytes
        df["Flow Bytes/s"] = df["Flow Bytes/s"].replace('Infinity', -1)
        df["Flow Bytes/s"] = df["Flow Bytes/s"].replace('NaN', 0)
        number_or_not=[]
        for item in df["Flow Bytes/s"]:
            try:
                k=int(float(item))
                number_or_not.append(int(k))
            except:
                number_or_not.append(item)
        df["Flow Bytes/s"] = number_or_not
                

        # process objects
        labelencoder_X = preprocessing.LabelEncoder()

        for label in self._LABELS:
            if not df[label].dtype=="object":
                continue
            try:
                df[label]=labelencoder_X.fit_transform(df[label])
            except:
                df[label]=df[label].replace('Infinity', -1)

        
        
        temp_file = tempfile.TemporaryFile(mode="w+", delete=False)
        df.to_csv(temp_file.name ,index = False)
        return temp_file.name

    def _predict(self, processed_csv: pathlib.Path) -> TaskResult:
        feature_list=list(self._LABELS[:-1])

        df=pd.read_csv(processed_csv,usecols=feature_list)
        df=df.fillna(0)

        X = df[feature_list]
        print("model", pathlib.Path(__file__).resolve().parent / "resources" /"model.pkl")
        model = joblib.load(
            str(pathlib.Path(__file__).resolve().parent / "resources" /"model.pkl")
        )

        prediction = model.predict(X)
        print(prediction)
        print(int(np.sum(prediction)), int(len(prediction) - np.sum(prediction)))
        return TaskResult(
            benign_thread=int(np.sum(prediction)),
            attack_thread=int(len(prediction) - np.sum(prediction))
        )

