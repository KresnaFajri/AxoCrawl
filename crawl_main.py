import requests
import pandas as pd
import json
import time
from AxoCrawl.utils import ReadData,JSONStore
from AxoCrawl.spiders.crawler import DDGSearchCrawler
from config import CrawlConfig

if __name__ == "__main__":
    #Read Data from .csv for .xlsx
    reader = ReadData(filepath=CrawlConfig.DATA_PATH, 
                      column="nama_produk_pendek")
    
    products=reader.get_product_names()
    print(type(CrawlConfig.MAX_RETRIES))
    #Define crawler
    store = JSONStore(filepath=CrawlConfig.STORE_PATH)
    crawler = DDGSearchCrawler(threshold=CrawlConfig.FUZZY_THRESHOLD,
                               max_retries = CrawlConfig.MAX_RETRIES,
                               delay = CrawlConfig.DELAY)
    
    #DECIDING STAGE
    #CHOOSE, 1.Rewrite all records.. or 2.Keep written records and scrape the rest?

    if CrawlConfig.MODE == 'REWRITE':
        print(f"[MODE : REWRITE] All records will be rewritten")
        existing = {}
        
    elif CrawlConfig.MODE == 'UPDATE':
        print(f"[MODE :UPDATE] - Only crawl unmatched products and keep the rest")
        existing = store.load()

    total = len(products)    
    skipped = 0
    crawled = 0

    for i,product_name in enumerate(products):
        if CrawlConfig.MODE == 'UPDATE' and not store.need_crawl(product_name,existing):

            print(f"[{i+1}/{total} SKIPPING {product_name}, already matched]")

            skipped += 1
            
            continue

        print(f"[{i+1}/{total}] Crawling:{product_name} ingredients")
        results = crawler.search(product_name)

        MATCHES = [r for r in results if r["is_match"]]

        print(f" {len(MATCHES)} match from {len(results)} results")

        for m in MATCHES:
            print(f"     ✓ [{m['similarity_score']}] {m['title']}")
        
        existing[product_name] = results

        crawled += 1

        #Save to JSON
        store.save(existing)

        time.sleep(CrawlConfig.DELAY)

    print(f"\nSelesai!")
    print(f"  Crawled : {crawled} produk")
    print(f"  Skipped : {skipped} produk")
    print(f"  Total   : {total} produk")
    print(f"  Output  : {CrawlConfig.STORE_PATH}")