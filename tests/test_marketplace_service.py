import json
import unittest
from unittest.mock import patch, MagicMock
from typing import List
from requests import Response, Timeout

from services.marketplace_service import print_seller_info_with_products_price_above_100, get_sellers_request


class TestMainFunctions(unittest.TestCase):

    @patch('builtins.print')
    def test_print_seller_info_with_products_price_above_100(self, mock_print: MagicMock) -> None:
        with open('test_data.json', 'r') as file:
            data = json.load(file)

        result: List[dict] = print_seller_info_with_products_price_above_100(data)

        expected_length: int = 15
        self.assertEqual(len(result), expected_length)
        mock_print.assert_called()

    @patch('services.marketplace_service.requests.get')
    @patch('services.marketplace_service.logging')
    def test_get_sellers_request_success(self, mock_logging: MagicMock, mock_requests_get: MagicMock) -> None:
        mock_response: Response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_requests_get.return_value = mock_response

        response: Response = get_sellers_request()

        self.assertEqual(response, mock_response)
        mock_logging.info.assert_called_with('Status Code: 200')

    @patch('services.marketplace_service.requests.get')
    @patch('services.marketplace_service.logging')
    def test_get_sellers_request_400_error(self, mock_logging: MagicMock, mock_requests_get: MagicMock) -> None:
        mock_response: Response = MagicMock(spec=Response)
        mock_response.status_code = 400
        mock_requests_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_sellers_request()

        mock_logging.error.assert_called_with('Bad Request: Check the request parameters.')

    @patch('services.marketplace_service.requests.get')
    @patch('services.marketplace_service.logging')
    def test_get_sellers_request_404_error(self, mock_logging: MagicMock, mock_requests_get: MagicMock) -> None:
        mock_response: Response = MagicMock(spec=Response)
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_sellers_request()

        mock_logging.warning.assert_called_with('No marketplace found.')

    @patch('services.marketplace_service.requests.get')
    @patch('services.marketplace_service.logging')
    def test_get_sellers_request_500_error(self, mock_logging: MagicMock, mock_requests_get: MagicMock) -> None:
        mock_response: Response = MagicMock(spec=Response)
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        with self.assertRaises(Exception):
            get_sellers_request()

        mock_logging.error.assert_called_with('Internal Server Error: Retry or report the issue.')

    @patch('services.marketplace_service.requests.get')
    @patch('services.marketplace_service.logging')
    def test_get_sellers_request_timeout_error(self, mock_logging: MagicMock, mock_requests_get: MagicMock) -> None:
        mock_requests_get.side_effect = Timeout
        with self.assertRaises(Timeout):
            get_sellers_request()

        mock_logging.error.assert_called_with(
            'Request Timeout: The server did not respond within the specified timeout.'
        )


if __name__ == '__main__':
    unittest.main()
