from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

URL_BASE = "https://alabamatienda.com.ar"

INPUT_DIR = "input"
OUTPUT_DIR = "output"
Path(OUTPUT_DIR).mkdir(exist_ok=True, parents=False)

OUTPUT_LOG = f"{OUTPUT_DIR}/alabama.log"
OUTPUT_PRODUCTS = f"{OUTPUT_DIR}/output.json"

PROXY = {
    'http': os.environ.get('PROXY'), 
    'https': os.environ.get('PROXY') 
}

HEADERS = {
    'accept': 'image/webp, application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://alabamatienda.com.ar/search/?q=remera&mpage=4',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Google Chrome";v="157", "Chromium";v="157"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

PARAMS = {
    'q': 'remera',
    'results_only': 'true',
    'limit': '12',
    'theme': 'rio',
    'nube_sdk': '1',
}

MAX_ATTEMPTS = 3