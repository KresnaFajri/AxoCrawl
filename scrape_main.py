import json
import pandas as pd
import time
import os
from config import CrawlConfig
from AxoCrawl.spiders.scraper import IngredientScraper

#Config
JSON_PATH = CrawlConfig.STORE_PATH
EXCEL_PATH = CrawlConfig.DATA_PATH
DELAY = CrawlConfig.DELAY

def main():
    df = pd.read_excel(EXCEL_PATH)

    with open(JSON_PATH, 'r',encoding="utf-8") as f:
        data = json.load(f)

    scraper = IngredientScraper()
    scraped_products = set()

    ingredients_map = {}

    for item in data:
        url = item.get("link","")
        product = item.get("product","")
        if product in scraped_products:
            print(f'[DATA ALREADY EXIST] -> Skipping {product}')
            continue

        #Skipping unrelated/unsupported domains
        if not scraper.is_supported(url):
            continue

        print(f"\nScraping: {product}")
        print(f"URL : {url}")

        ingredients = scraper.scrape(url)

        if ingredients:
            ingredients_str = ", ".join(ingredients)
            print(f" ✓ {len(ingredients)} ingredients ditemukan")
            ingredients_map[product]=ingredients_str
            scraped_products.add(product)

            time.sleep(DELAY)
            continue
        print(f"  ✗ Tidak ada ingredients ditemukan")
        time.sleep(DELAY)
    df['ingredients'] = df['nama_produk_pendek'].map(ingredients_map)
    output_path = EXCEL_PATH.replace(".xlsx","_ingredients.xlsx")
    df.to_excel(output_path,index=False)
    print(f"[SCRAPING FINISHED] -> File is saved and edited as {output_path}")
if __name__ == "__main__":
    main()
        
