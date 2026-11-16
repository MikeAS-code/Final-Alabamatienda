import json

from curl_cffi import requests
from lxml import html

headers = {
    "accept": "image/webp, application/json",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://alabamatienda.com.ar/search/?q=campera",
    "sec-ch-ua": '"Not-A.Brand";v="99", "Microsoft Edge";v="157", "Chromium";v="157"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157.0.0.0",
    "x-requested-with": "XMLHttpRequest",
}

params = {
    "q": "Campera",
    "results_only": "true",
    "limit": "12",  # Limitado a 12
    "theme": "rio",
    "nube_sdk": "1",
}

page = 1

response = requests.get(
    f"https://alabamatienda.com.ar/search/page/{page}/", params=params, headers=headers
)

response = response.json()

print(len(response.get("nube_sdk_products")))
#print(response.get("page"))
#print(response.get("has_results"))
#print(response.get("has_next"))

with open("./index.html", "wb") as f:
    f.write(bytes(response["html"], encoding="utf-8"))

tree = html.fromstring(response.get("html"))

divs = tree.xpath("//div[contains(@data-variants, 'available')]/@data-variants")

for div in divs:
    print(json.loads(div)[0]['image_url'])
    print(json.loads(div)[0]['available'])
    print(json.loads(div)[0]['discount_percentage_number'])
