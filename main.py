import logging

from requests import Response
from services.marketplace_service import (
    get_sellers_request,
    get_sellers,
    print_seller_info_with_products_price_above_100
)

logging.basicConfig(level=logging.INFO)


def fetch_marketplace_data() -> Response:
    try:
        marketplace_data = get_sellers_request()
        if marketplace_data:
            print_seller_info_with_products_price_above_100(get_sellers(marketplace_data))
        return marketplace_data
    except Exception as e:
        logging.warning(f'Something went wrong: {str(e)}')


if __name__ == '__main__':
    fetch_marketplace_data()
