import config
import pandas as pd
import time
import random
import json
from curl_cffi import requests
from lxml import html
from log import Log

logger = Log.get_logger(config.OUTPUT_LOG)


class PDP:
    def __init__(self):
        pass

    def run(self):
        logger.info("PDP started")
        # Copy inputs to dict
        inputs = pd.read_csv(
            f"{config.INPUT_DIR}/product.csv", usecols=["query"])
        results_input = inputs.to_dict(orient="list")


        record_final = []
        for key in results_input:
            for query in results_input[key]:
                record = {
                    "query": "",
                    "data": []
                }
                
                logger.info(f"KEY {query}")
                record["query"] = query
                record["data"] = self.get_products_by_query(query)
                record_final.append(record)

        with open(config.OUTPUT_PRODUCTS, mode="w", encoding="utf-8") as f:
            json.dump(record_final, f)
            
        logger.info("PDP finished")

    def get_products_by_query(self, query):
        logger.info(f"Obteniendo resultados para: {query}")
        params = config.PARAMS.copy()
        params["q"] = query
        #logger.info(params)
        flag = True
        count = 1
        products_final = []
        while(flag):
            response = self.make_requests(
                        url=f"https://alabamatienda.com.ar/search/page/{count}/",
                        proxies=config.PROXY,
                        headers=config.HEADERS,
                        params=params,
                        timeout=20)
            
            logger.info(f"Recuperando datos del paginado{count}")
            if response.json()["has_results"] == False:
                flag = False
                break
            products = response.json()["nube_sdk_products"]
            for product in products:
                products_final.append(self.clean_product(product))
            count += 1
        return products_final
                
            
    def clean_product(self, product):
        #logger.info(f"cleaning for{product.get("canonical_url")}")
        try:
            url = product.get("canonical_url")
        except:
            logger.error("Error getting URL")
            
        try:
            id = product.get("id")
        except:
            logger.error("Error getting id")
        
        try:
            name = product.get("name").get("es")
        except:
            logger.error("Error getting name")
        
        try:
            description = product.get("description").get("es") or None
        except:
            logger.error("Error getting description")
        
        try:
            categories_final = []
            category_list = product.get("categories")
            for category in category_list:
                categories_final.append(category.get("name"))
        except:
            logger.error("Error getting categories")
        
        try:
            images_final = []
            images = product.get("images")
            for image in images:
                images_final.append(image.get("src"))
                
        except:
            logger.error("Error getting images")
        
        # VARIANTES
        try:
            variants_final = []
            variants = product.get("variants")
            for variant in variants:
                 
                try:
                    id_variant = variant.get("id")
                except:
                    logger.error("Error getting variant id")
                
                try:
                    group_id = variant.get("product_id")
                except:
                    logger.error("Error getting group id")
                                
                try:
                    price = variant.get("price")
                except:
                    logger.error("Error getting price")
                    
                try:
                    list_price = variant.get("price")
                except:
                    logger.error("Error getting price")
                
                try:
                    options_aux = variant.get("options")
                    options_final = []
                    record_variant_option = {
                        "name": "",
                        "value": ""
                    }
                # Opciones de variante    
                    for option in options_aux:
                        name_record_final = option.get("name")
                        value_record_final = option.get("value")
                        record_variant_option["name"]= name_record_final
                        record_variant_option["value"]= value_record_final
                        options_final.append(record_variant_option)
                except:
                    logger.error("Error getting variant options")
                    
                record_variant = {
                                    "id": id_variant,
                                    "group_id": group_id,
                                    "price": price,
                                    "list_price": "",
                                    "discount_percentage": "",
                                    "available": "",
                                    "options": options_final,
                                }
                variants_final.append(record_variant)
        except:
            logger.error("Error getting variants")
            
        record = {
            "url": url,
            "id": id,
            "name": name,
            "description": description,
            "category_list": categories_final,
            "images": images_final,
            "variants": variants_final,
        }
        return record
    
    def make_requests(self,
                      url,
                      proxies={},
                      headers={},
                      params={},
                      impersonate="chrome",
                      timeout=20):
        for attempt in range(config.MAX_ATTEMPTS):
            try:
                response = requests.get(
                    url=url,
                    params=params,
                    proxies=proxies,
                    headers=headers,
                    impersonate=impersonate,
                    timeout=timeout)

                if response and response.status_code == 200:
                    return response

                time.sleep(random(2, 4))

            except Exception as e:
                logger.error(f"Error reaching {url} - ATTEMPT {attempt}/{config.MAX_ATTEMPTS}")
        logger.error(
            f"Max attempts reached",
            f"There was a problem getting {url} - {e}")


class Discovery:
    def __init__(self):
        pass


if __name__ == "__main__":
    logger.info("Crawler init")
    PDP().run()
    logger.info("Crawler finish")
