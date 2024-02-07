import requests
import json
import logging

from requests import Response, RequestException, Timeout
from retrying import retry
from resources.configuration import (
    MOCK_ENDPOINT_URL,
    TIMEOUT_SECONDS,
    MIN_PRODUCT_PRICE,
    MIN_PRODUCTS_COUNT,
    RETRY_MAX_ATTEMPTS,
    RETRY_WAIT_MULTIPLIER
)


@retry(
    stop_max_attempt_number=RETRY_MAX_ATTEMPTS,
    wait_exponential_multiplier=RETRY_WAIT_MULTIPLIER,
    retry_on_exception=lambda e: isinstance(e, RequestException)
)
def get_sellers_request() -> Response:
    try:
        response = requests.get(MOCK_ENDPOINT_URL, timeout=TIMEOUT_SECONDS)
        logging.info(f'Status Code: {response.status_code}')
        if response.status_code == 400:
            logging.error('Bad Request: Check the request parameters.')
            raise RequestException
        elif response.status_code == 404:
            logging.warning('No marketplace found.')
            raise RequestException
        elif response.status_code == 500:
            logging.error('Internal Server Error: Retry or report the issue.')
            raise RequestException
        else:
            response.raise_for_status()
        return response
    except Timeout:
        logging.error('Request Timeout: The server did not respond within the specified timeout.')
        raise


def get_sellers(marketplace_data: Response) -> list:
    try:
        sellers = marketplace_data.json()
        return sellers
    except json.JSONDecodeError as e:
        logging.error(f'Error decoding JSON response: {e}')
        raise json.JSONDecodeError


def print_seller_info_with_products_price_above_100(sellers: list) -> list:
    count = 1
    sellers_with_products_price_above_100 = []
    for seller in sellers:
        if seller['products'] is None:
            continue
        products_above_100 = [
            product
            for product in seller['products']
            if product.get('product_price') is not None
            and product.get('product_price') > MIN_PRODUCT_PRICE
        ]
        if len(products_above_100) >= MIN_PRODUCTS_COUNT:
            print(f'{count}) Seller: {seller.get("seller_first_name")} {seller.get("seller_last_name")},'
                  f' Rating: {seller.get("rating")}')
            print('Products:')
            for product in products_above_100:
                print(
                    f' - {product.get("product_name")}, Price: {product.get("product_price")},'
                    f' In stock: {product.get("product_quantity")}'
                )
            print('\n')
            seller_with_products_price_above_100 = seller
            seller_with_products_price_above_100['products'] = products_above_100
            sellers_with_products_price_above_100.append(seller_with_products_price_above_100)
            count += 1
    return sellers_with_products_price_above_100
