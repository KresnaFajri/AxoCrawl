import os
import json
import pandas as pd
from pathlib import Path

class ReadData:
    def __init__(self, filepath:str, column:str):
        self.filepath = filepath
        self.column = column

    def get_product_names(self)-> list:
        if self.filepath.endswith('.csv'):
            df = pd.read_csv(self.filepath)
            return df[self.column].dropna().tolist()
        
        elif self.filepath.endswith(".xlsx"):
            df = pd.read_excel(self.filepath)
            return df[self.column].dropna().tolist()
        
        else:
            print("Error, can't read files")

class JSONStore:
    def __init__(self, filepath:str):
        self.filepath = filepath
    
    def load(self)->dict:
        """
        Load existing JSON, return dict {product_name:[results]}
        """
        if not os.path.exists(self.filepath):
            return {}
        with open(self.filepath, "r",encoding="utf-8") as f:
            data = json.load(f)

        #Conversion list of results to dict 
        store = {}
        for item in data:
            product = item["product"]
            if product not in store:

                store[product] = []

            store[product].append(item)
        return store
    
    def save(self, store:dict):
        """
        Save dict {product : [results] to json as flat list}
        """
        flat = []
        for results in store.values():
            flat.extend(results)

        with open(self.filepath,"w",encoding="utf-8") as f:

            json.dump(flat, f, indent=2, ensure_ascii=False)

    def need_crawl(self, product:str, store:dict)->bool:
        """
        Check if data needs to be crawl again or not.
        """
        if product not in store:
            return True
        
        results = store[product]

        has_match=any(r["is_match"] for r in results)

        return not has_match

