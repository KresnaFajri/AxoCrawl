import requests 
import pandas as pd
import json
from bs4 import BeautifulSoup

class IngredientScraper:
    SUPPORTED_DOMAINS = ["cosdna.com","incidecoder.com","skinsort.com"]
    HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    def is_supported(self,url:str):
        return any(domain in url for domain in self.SUPPORTED_DOMAINS)
    
    def detect_domain(self,url:str)->str:
        for domain in self.SUPPORTED_DOMAINS:
            if domain in url:
                return domain
        return None
        
    # --CosDNA--
    def scrape_CosDNA(self,url:str)->list:
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            ingredients = []

            #Take every <li>
            items = soup.select("ul.ings-list li")

            for item in items:
                span = item.select_one("span.colors")

                if span:
                    name = span.get_text().strip()
                    if name:
                        ingredients.append(name)
            return ingredients
        except Exception as e:
            print(f"Data not found in CosDNA:{e}")
            return []


    def scrape_inci(self, url:str)->list:
        ingredients = []
        try:
            tables = pd.read_html(url)
            if tables:
                tables = tables[0]
                ingredients = tables.iloc[:,0].dropna().tolist()
                ingredients = [str(i).strip() for i in ingredients]
        except:
            pass
        return ingredients
    
    def scrape_skinsort(self, url:str)->list:
        try:
            response = requests.get(url, headers = self.HEADERS, timeout =10)

            #Check if there's login page
            if "sign up" in response.text.lower() or "upgrade" in response.text.lower():
                print(f"Sign Up Sessions. Need credentials")
                return []
            soup = BeautifulSoup(response.text,'html.parser')

            #Absorb ingredients data
            ingredients = []
            items = soup.select("span[data-ingredient-name-for]")
            for item in items:
                p = item.find("p")
                if p:
                    ingredients.append(p.get_text().strip())
            return ingredients
        
        except Exception as e:
            print(f"Failed absorbing data from Skinsort")
            return []
        # -----------------------------
    def scrape(self, url:str)-> list:
        domain = self.detect_domain(url)
        if domain == "cosdna.com":
            return self.scrape_CosDNA(url)
        elif domain == "incidecoder.com":
            return self.scrape_inci(url)
        elif domain == 'skinsort.com':
            return self.scrape_skinsort(url)
        return []