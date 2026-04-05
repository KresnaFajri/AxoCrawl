import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = r"C:\Kresna Folder\KERJAAN\NOSE HERBAL\Tools\AxoCrawl"
load_dotenv()

class CrawlConfig:
    DATA_PATH = os.getenv("DATA_PATH")
    STORE_PATH = os.getenv("STORE_PATH")
    DELAY = int(os.getenv('DELAY'))
    MODE = os.getenv("MODE")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES"))
    FUZZY_THRESHOLD= float(os.getenv("FUZZY_THR"))
    