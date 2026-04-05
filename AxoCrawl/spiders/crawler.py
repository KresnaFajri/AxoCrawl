import sys
import os
from rapidfuzz import fuzz
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import requests
from bs4 import BeautifulSoup
import pandas as pd
from AxoCrawl.utils import ReadData
from duckduckgo_search import DDGS

#Use duckduckgo-search 
class DDGSearchCrawler:
    def __init__(self, threshold:int =70, max_retries:int=4,delay:float=3):
        self.threshold = threshold
        self.max_retries=max_retries
        self.delay=delay

    def __score(self, product_name: str,title:str)->int:
        #Calculate fuzzy score between searched product_name and found website name
        return fuzz.token_set_ratio(product_name.lower(),title.lower())

    def search(self, product_name:str) -> list:
        query = f"{product_name} ingredients"
        results = []

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f" attempt {attempt}/{self.max_retries}...")

                with DDGS() as ddgs:
                    search_results = list(ddgs.text(query, 
                                               max_results=10))

                    if search_results:
                        for item in search_results:
                            title = item.get("title","")
                            score = self.__score(product_name,title)
                            results.append({
                                "product":product_name,
                                "title":title,
                                "link":item.get("href"),
                                "snippet":item.get("body"),
                                "similarity_score":score,
                                "is_match": score >= self.threshold
                            })
                        break
                    else:
                        print(f" Data is empty, retry after {self.delay}s...")
                        time.sleep(self.delay)
            
            except Exception as e:
                    print(f"Error in searching {product_name} : \n {e}")
                    time.sleep(self.delay)

        results.sort(key=lambda x:x["similarity_score"],reverse=True)
        return results