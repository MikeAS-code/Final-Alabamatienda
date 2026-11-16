import pandas as pd
import csv
import json
import config
import time
import random
from pathlib import Path
from lxml import html
from curl_cffi import requests
from log import Log
logger = Log.get_logger('scraper.log')


class Crawler:

    def __init__(self):
        self.querys = []
        self._records = []

    def read_input(self):
        with open('./input/product.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=' ')
            for row in csvreader:
                if row[0] != 'query':
                    self.querys.append(row[0])

    def make_requests(self,
                      url,
                      status_code=200,
                      proxies={},
                      headers={},
                      cookies={},
                      params={},
                      payload={},
                      impersonate='chrome',
                      verify=False):
        attempt = 1
        while attempt <= config.MAX_RETRIES:
            try:
                response = requests.get(url=url,
                                        proxies=proxies,
                                        headers=headers,
                                        cookies=cookies,
                                        params=params,
                                        data=payload,
                                        impersonate=impersonate,
                                        verify=verify)
                if response and response.status_code == status_code:
                    return response
                else:
                    raise Exception(f'Error on requests. Status code: {response.status.code}')
            except Exception as e:
                logger.error(f'Attempt {attempt}. Error: {e}')
                attempt += 1
                time.sleep(random.randint(2,4))
        logger.info('Max attempts reached')
        return None
    
    def get_products(self):
        try: 
            for query in self.querys:
                datos = []
                page=1
                flag=True
                while flag:
                    params = {
                        'q': query,
                        'results_only': 'true',
                        'limit': '',
                        'theme': 'rio',
                        'nube_sdk': '1',
                    }

                    res = self.make_requests(url=f'https://alabamatienda.com.ar/search/page/{page}/',
                                             headers=config.HEADERS,
                                             proxies=config.PROXIES,
                                             params=params)
                    if res:
                        data = json.loads(res.content)
                        if data.get('has_results') == False:
                            if page == 1:
                                logger.info(f'Sin resultados para {query}')
                                self._records.append({
                                    'query': query,
                                    'data': []
                                })
                            flag=False
                            break
                        try:
                            products = data.get('nube_sdk_products')
                            producsthtml = None
                            try:
                                productss = data.get('html')
                                tree = html.fromstring(productss)
                                producsthtml = json.loads(tree.xpath('.//div[contains(@class,"js-product-container")]/@data-variants')[0])
                            except:
                                logger.exception('Error al obtener html')
                            try:
                                for product in products:
                                    datos.append(self.get_data_products(product,producsthtml))
                            except:
                                logger.exception('')
                            page += 1
                        except Exception as e:
                            logger.exception('Error al obtener datos')
                self._records.append({
                    'query': query,
                    'data': datos
                })
                        
        except:
            logger.exception('Error al obtener productos')

    def get_data_products(self,product,producthtml):
        url = product.get('canonical_url')
        id = product.get('id')
        name = product.get('name',{}).get('es')
        if name:
            name=name.strip()
        description = product.get('description',{}).get('es')
        categories = product.get('categories',[])
        category_list = []
        try:
            for categorie in categories:
                category_list.append(categorie.get('name'))
        except:
            logger.info('No hay categories')
        images = product.get('images',[])
        images_list = []
        try:
            for image in images:
                images_list.append(image.get('src'))
        except:
            logger.info('No hay images')
        variants = product.get('variants',[])
        variants_list = []
        try:
            for variant in variants:
                available = None
                discount = None
                idvariante = variant.get('id')
                if producthtml:
                    for p in producthtml:
                        if p.get('product_id') == id:
                                if p.get('id') == idvariante:
                                    available = p.get('available')
                                    discount = p.get('discount_percentage_number')
                else: 
                    available = None
                    discount = None
                options = variant.get('options', None)
                if options:
                    options = options[0]
                price = variant.get('price')
                if variant.get('has_promotional_price'):
                    list_price = variant.get('compare_at_price')
                else:
                    list_price = price

                datos = {
                    'id' : id,
                    'group_id': id,
                    'price': price,
                    'list_price': list_price, 
                    'available': available,
                    'discount_percentage': discount,
                    'options': options
                }
                variants_list.append(datos)
        except:
            logger.exception('No hay variantes')
          

        producto = {
            "url": url,        
            "id": id,        
            "name": name,       
            "description": description,        
            "category_list": category_list,        
            "images": images_list,
            "variants": variants_list  
        }
        return producto    

    def save_data(self):
        try:
            #df = pd.DataFrame(self._records,index=False)
            #df.to_json('output/output.json')
            Path('output').mkdir(exist_ok=True,parents=False)
            with open("output/output.json", encoding="utf-8", mode="w") as f:
                json.dump(self._records, f)
        except:
            logger.exception('Error al guardar datos')


    def run(self):
        self.read_input()
        self.get_products()
        self.save_data()

if __name__ == '__main__':
    Crawler().run()
