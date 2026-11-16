import os
import re

from dotenv import load_dotenv

load_dotenv(".env")

TIMEOUT = 30
MAX_RETRIES = 3

PROXY = os.getenv("PROXY")
PROXIES = {"http": PROXY, "https": PROXY}

SEARCH_URL = "https://alabamatienda.com.ar/search/page"

SEARCH_HEADERS = {
    'accept': 'image/webp, application/json',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://alabamatienda.com.ar/search/?q=campera',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Microsoft Edge";v="157", "Chromium";v="157"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36 Edg/157.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': '_ga=GA1.1.1634320227.1794833618; _fbp=fb.2.1794833618446.6407565233177176; tn_track=042736166eb04478453f9699898aa965a6f941a4~aef4e3ad93b1c9bcb9bf9a69a5bec2728d2afab5; x-rand-user=eeee414b972be76d6658f1e9970befc5b0664af5~9473; store_login_session=188ec317b056b02eab0639ec706f886c6d9e969a~7a4efd1f18556a76353720c0df425085845862f09b2a3c97ec6032a8fed244c6; _cfuvid=17l35.sSXWPjzopMsw3Mp2Zq6P5JUjE8wc.lfnnwAw4-1794833618.1075194-1.0.1.1-wmYGRwp9kJ_z6ZGOea9T_PEtd7guDJYtK9RKq54BvkQ; TPIDC=wg7qp-tkfpg14q-knv8o70rl4mgz5xa1-vrp9aboqfm18lxkg-5itku-mhpb; cwdlc=1; cus=false; _wpnlvusw=1; home_no_cache=0481ad5ce31d61476361c3348a19e971bb8f3fba~1; store_cart_session_1577745=6be646c8c5575d6e4ff10cb5a6e8e0389250dc28~eyJpdiI6InJOYitTZlhDQ0NHRXZtR3BqVUZnRUE9PSIsInZhbHVlIjoiQVZuVU1KenZ5SVRvV3RhTUNRTGFrUWRYUWl5VkdONHR4SHFXNnhMZVpaa1UwV09JT3pwQzd0WjNNdERrRnVZVyIsIm1hYyI6ImE1ODRiNjQ5NTY3Nzg2YmQ3MDU1MTUyMzBjOWM5NWU2MjE5OTEwYjU5ZGIyOGI2MjY4NzNmYjA4MGQwZTU0N2IifQ%3D%3D; __cf_bm=5m6hWc_CO8ucLDetC8Clku.gIeBropdERQ5Cbsm5.uc-1794837436.6006215-1.0.1.1-2HAohhgPssPYF.AGaKOQz_wLvgw_366NRx9LOwPHvZ7LNGbTd_TCTu2uuPdnopCa14p2UjHrgtdUAPzpOPXs7KdlYgxCyXIbbLn6Sz54uoAaZHZJ7Lw3VCFAzm1O1BNP; _ga_EQ81RSW3V1=GS2.1.s1794837436$o2$g1$t1794837438$j58$l0$h1365318061; wpnViewcount=20; tn_tracksession=00ed2c63767cbfdbded16eab70ba61da878da145~db3c01949fa67bec44bcb22a6a87e19992355293; store_session_payload_1577745=7138878f93fbb40e9ea54bef50e1b4f4a257049d~eyJpdiI6ImpWT3FxL3IrMVArYk04V1phRjdId3c9PSIsInZhbHVlIjoidldTRWlubXg5VGkycCtLdkFVcTY2RUtTbXdlNVp1M1RNVlcwUy9ENjNGaUNsbTJ5MGx4VHM5OFlmZ0RiaG0rVnhUeFFsaGNMc05pY0pETDNGd3N5aWJwMzF3clhzZ1lIVW05VXYxT3NPWVV1aWM4aCtJM1ZObXRRSkdYVGdSWnoxeGVzajRnbVpoMjZudHZkenpmUFZVVmJmMjFwVzQwQ3F2Q2Q2WGtvUGdINHYvRTJwVXdneVgvUWdoYitrTXhyVTFuS2NtNGpLQ3g5WTNtaG5XYTF4Zkg4U3lxbGk0V2s1N3c4MSs0ZVZhdHQxMGxXQ0RGcVoxZTJWNDZPZlZDOWdqK3R5ajZyNEl6ZUM2dTBTRWhxY0pwQ3JEUmcrR20rYUMzbHJhZXlKZS9WOVRPWUlJczlQY3R0RE5kRXBIWDA0T0FCK1JGZWp2STM2VVVBcjNHODBidHVmTG5KZGw5dkpDSjhmd0I3U1FzPSIsIm1hYyI6IjhjZmIyYzI1ZjZmOGVjMDliZmRhZjc1NDg3OTdjODU2M2QzNGQ4ZDE3Nzk0OGIyMDJmZGVlMjU4M2Y1MDI4ZmMifQ%3D%3D; _wpn_cotpc=1; sdtpc=1',
}

SEARCH_PARAMS = {
    'q': 'campera',
    'results_only': 'true',
    'limit': '12',
    'theme': 'rio',
    'nube_sdk': '1',
}