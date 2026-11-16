import os
from dotenv import load_dotenv

load_dotenv('.env')

PROXY = os.environ.get('PROXY')

PROXIES = {
    'http': PROXY,
    'https': PROXY
}

BASE_URL = 'https://alabamatienda.com.ar/'

HEADERS = {
    'accept': 'image/webp, application/json',
    'accept-language': 'es-ES,es;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://alabamatienda.com.ar/search/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Google Chrome";v="157", "Chromium";v="157"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36',
    #x-requested-with': 'XMLHttpRequest',
}

MAX_RETRIES = 3

# Your code here