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

    def test_update_currency_cache(self):
        mock_api_response_input = {"rates":{"USD":0.6541135574,"AUD":0.9421205098},"base":"NZD","date":"2020-07-07"}
        self.instance = Invoice(self.valid_input_data)
        self.instance.update_currency_cache(mock_api_response_input)
        self.assertEqual(
            self.instance.currency_cache,
            {"USD":0.6541,"AUD":0.9421}
        )
        # each value has 4 decimal places
        for key in self.instance.currency_cache.keys():
            self.assertEqual(
                len(str(self.instance.currency_cache[key]).split('.')[1]),
                4
            )

    def test_generate_request_items(self):
        self.instance = Invoice(self.valid_input_data)
        self.instance.currency_cache = {}
        self.assertEqual(
            self.instance.generate_request_items().sort(),
            ["AUD","USD"].sort()
        )
        self.instance.currency_cache = {"AUD"}
        self.assertEqual(
            self.instance.generate_request_items().sort(),
            ["USD"].sort()
        )
        self.instance.currency_cache = {"AUD","USD"}
        self.assertEqual(
            self.instance.generate_request_items(),
            []
        )

    @responses.activate
    def test_calculate_line_total(self):
        responses.add(
            responses.GET,
            settings.EXCHANGE_RATES_API_URL + '/' + self.input_date,
            json={"rates":{"AUD":0.9421205098,"USD": 0.6541135574},"base":"NZD","date":"2020-07-07"},
            status=200
        )
        mock_line_usd = {"description":"Intel Core i9","currency":"USD","amount":700}
        self.instance = Invoice(self.valid_input_data)
        self.instance.prepare_currency_cache()
        self.assertEqual(
            self.instance.calculate_line_total(mock_line_usd),
            1070.17
        )
        mock_line_aud = {"description":"Intel Core i9","currency":"AUD","amount":500}
        self.assertEqual(
            self.instance.calculate_line_total(mock_line_aud),
            530.73
        )

    @responses.activate
    def test_calculate_invoice_total(self):
        responses.add(
            responses.GET,
            settings.EXCHANGE_RATES_API_URL + '/' + self.input_date,
            json={"rates":{"AUD":0.9421205098,"USD": 0.6541135574},"base":"NZD","date":"2020-07-07"},
            status=200
        )
        self.instance = Invoice(self.valid_input_data)
        self.instance.prepare_currency_cache()
        self.instance.lines = [
            {"description":"Intel Core i9","currency":"USD","amount":700},
            {"description":"ASUS ROG Strix","currency":"AUD","amount":500}
        ]
        self.assertEqual(
            self.instance.calculate_invoice_total(),
            "{:.2f}".format(1600.90)
        )

