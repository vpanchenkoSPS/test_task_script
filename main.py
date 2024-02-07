from __future__ import annotations

import logging

from requests import Response, RequestException
from services.marketplace_service import (
    get_sellers_request,
    get_sellers,
    print_seller_info_with_products_price_above_100
)

logging.basicConfig(level=logging.INFO)


def fetch_marketplace_data() -> Response | list:
    try:
        marketplace_data = get_sellers_request()
        if marketplace_data:
            return print_seller_info_with_products_price_above_100(get_sellers(marketplace_data))
        return marketplace_data
    except RequestException as e:
        logging.warning(f'There was an ambiguous exception that occurred while handling your request.: {str(e)}')


if __name__ == '__main__':
    fetch_marketplace_data()
