from src.calculate_invoice import Invoice
import src.settings as settings

import unittest,responses

class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.valid_input_data = {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        self.input_date="2020-07-07"

    @responses.activate
    def test_retrieve_exchangerate_from_api_should_get_result_from_api(self):
        expected_result={"rates":{"AUD":0.9421205098,"USD": 0.6541135574},"base":"NZD","date":"2020-07-07"}
        base_currency="NZD"
        requested_currency=["AUD","USD"]

        responses.add(
            responses.GET,
            settings.EXCHANGE_RATES_API_URL + '/' + self.input_date,
            json=expected_result,
            status=200
        )

        self.instance = Invoice(self.valid_input_data)
        resp = self.instance.retrieve_exchangerate_from_api(requested_currency)
        self.assertEqual(
            resp,
            expected_result
        )

    @responses.activate
    def test_retrieve_exchangerate_from_api_can_handle_api_exceptions(self):
        input_date="2020-07-07"
        requested_currency=["AUD","USD"]
        responses.add(
            responses.GET,
            settings.EXCHANGE_RATES_API_URL + '/' + self.input_date,
            json={"error": "API malfunctioning"},
            status=503
        )
        with self.assertRaises(SystemExit) as custom_exception:
            self.instance = Invoice(self.valid_input_data)
            resp = self.instance.retrieve_exchangerate_from_api(requested_currency)
        self.assertEqual(custom_exception.exception.code,8)

    @responses.activate
    def test_retrieve_exchangerate_from_api_can_handle_invalid_data(self):
        input_date="2020-07-07"
        requested_currency=["AUD","USD"]
        responses.add(
            responses.GET,
            settings.EXCHANGE_RATES_API_URL + '/' + self.input_date,
            json={"rates":{"AUD":-0.9421205098,"USD": -0.6541135574},"base":"NZD","date":"2020-07-07"},
            status=200
        )
        with self.assertRaises(SystemExit) as custom_exception:
            self.instance = Invoice(self.valid_input_data)
            resp = self.instance.retrieve_exchangerate_from_api(requested_currency)
        self.assertEqual(custom_exception.exception.code,9)