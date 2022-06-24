import pandas as pd
import json

class LoadFiles():

    def __init__(self, *args) -> None:
        self.files = args[0]

    def loadjson(self):
        json_files = []
        for file in [f for f in self.files if f.endswith('json')]:
            jsonfile = open(file)
            json_files.append(json.load(jsonfile))
        return json_files

    def loadcsv(self):
        csv_files = []
        for file in [f for f in self.files if f.endswith('.csv')]:
            csv_files.append(pd.read_csv(file, index_col=False))
        return csv_files