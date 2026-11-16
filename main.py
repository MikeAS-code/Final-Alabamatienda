import pandas
from curl_cffi import requests
from lxml import html, etree
import config
import time
import random
import json
from pprint import pp


def make_requests(
    url,
    status_code=200,
    proxies=config.PROXIES,
    headers={},
    cookies={},
    payload={},
    params={},
    impersonate="chrome",
    verify=False,
    timeout=30,
):
    attempt = 0
    while attempt < config.MAX_RETRIES:
        try:
            response =requests.get(
                url,
                proxies=proxies,
                headers=headers,
                cookies=cookies,
                params=params,
                data=payload,
                impersonate=impersonate,
                verify=verify,
                timeout=timeout,
            )

            if response and response.status_code == status_code:
                return response
            else:
                raise Exception('There was an error on response')

        except Exception as e:
            attempt+=1
            print(f"Attempt {attempt} Error: {e}")
            time.sleep(random.randint(2, 4))

    print('Max retries reached')
    return None

class ProductOut:

    def append_html_data(self, html_data):
        try:
            for data in html_data:
                for var in self.variants:
                    if var.get('id') == data.get('id'):
                        var['discount_percentage'] = data.get('discount_percentage_number')
                        var['available'] = data.get('available')
        except Exception as e:
            print(f"Error agregando datos de descuento y stock a {self.id} - {self.url} : e = {e}")

    def _parse_variant(self, variant):
        id = variant.get("id")
        group_id = self.id
        price = variant.get("price")
        if variant.get("has_promotional_price"):
            list_price = variant.get("compare_at_price")
            # TODO
            discount_percentage = None
        else:
            list_price = price
            discount_percentage = None
        # TODO
        available = None

        options = variant.get("options")

        '''
        for opt in options_list:
            option = {"name": None, "value": None}
            if "name" in opt.keys():
                option = opt.get("name")
            if "value" in opt.keys():
                option = opt.get("value")

            options.append(option)
        '''

        return {
            "id": id,
            "group_id": group_id,
            "price": price,
            "list_price": list_price,
            "discount_percentage": discount_percentage,
            "available": available,
            "options": options,
        }

    def __init__(self, data):
        # Assume data is the json
        self.url = data.get("canonical_url")
        self.id = data.get("id")
        if data.get("name"):
            self.name = data.get("name").get("es")
        self.description = data.get("seo_description").get("es")

        categories = data.get("categories")
        self.category_list = []
        for cat in categories:
            if "name" in cat.keys():
                self.category_list.append(cat.get("name"))

        images = data.get("images")
        self.images = []
        for img in images:
            self.images.append(img.get("src"))

        self.variants = []

        variants_list = data.get("variants")

        for var in variants_list:
            self.variants.append(self._parse_variant(var))

        return

    def to_dict(self):
        return {
            "url": self.url,
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category_list": self.category_list,
            "images": self.images,
            "variants": self.variants,
        }

    #Para el set()
    def __hash__(self):
        return self.id
        pass


class PDP:
    def __init__(self):
        pass

    def process_product(self, data):
        return

    def run():
        return


class Discovery:
    def __init__(self):
        self.out_list = []
        self._query_records = set()
        self.index = 0
        pass

    def process_page(self, url, params):

        print(f"Procesando {params['q']} - Pagina {self.index}")

        page_results = set()

        response = make_requests(url, params=params, headers=config.SEARCH_HEADERS)
        if response.status_code == 200:
            data = json.loads(response.text)
            if not data.get('has_results'):
                print("NO HAY RESULTADOS")
                return False
            data_html = data.get('html')
            data_json = data.get('nube_sdk_products')
            for data_prod in data_json:
                prod = ProductOut(data_prod)
                print(f"Se encontro: {prod.name}")
                page_results.add(prod)

            tree = html.fromstring(data_html)
            html_divs = tree.xpath("//div[contains(@data-variants, 'available')]/@data-variants")
            #print(len(html_divs))
            html_data_list = []
            for div in html_divs:
                html_data_list.append(json.loads(div))


            # Hay como 10 formas mejores de hacer esto pero no se me occuren
            for html_data in html_data_list:
                for prod in page_results:
                    if html_data[0].get('product_id') == prod.id:
                        #print('ward')
                        prod.append_html_data(html_data)
                        continue
            has_next = data.get('has_next')
        else:
            raise ValueError(f"Request a {url} dio un status code incorrecto: response.status_code = {response.status_code}")

        self._query_records.update(page_results)
        self.index += 1

        return has_next

    def run(self, query):

        for q in query:
            self._query_records = set()
            self.index = 1
            q = q.get("query")
            q_run = {"query": q, "data": []}

            params = {
                "q": q,
                "results_only": "true",
                "limit": "12",
                "theme": "rio",
                "nube_sdk": "1",
            }

            has_next = self.process_page(f"{config.SEARCH_URL}/{self.index}", params)

            while has_next:
                has_next = self.process_page(f"{config.SEARCH_URL}/{self.index}", params)

            query_data = []
            for prod in self._query_records:
                query_data.append(prod.to_dict())
            self.out_list.append({
                'query': q,
                'data': query_data
            })

        return self.out_list


if __name__ == "__main__":
    query_csv = pandas.read_csv(r"input/product.csv").to_dict(orient="records")
    print(query_csv)
    out_list = Discovery().run(query_csv)

    df = pandas.DataFrame(out_list)

    df.to_json('./output.json')
    pass
