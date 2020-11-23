from src.process_input import ProcessInputFile
import src.settings as settings

import unittest


class TestProcessInputFile(unittest.TestCase):

    def setUp(self):
        self.input_filepath = settings.TEST_FIXTURE_ITEM
        print("===============",settings.TEST_FIXTURE_ITEM)

    def test_read_json_can_read_valid_input_file(self):
        self.instance = ProcessInputFile(self.input_filepath)
        self.assertEqual(
            self.instance.input_data,
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        )

    def test_read_json_reject_invalid_input_file_path(self):
        self.input_filepath_invalid = ''
        with self.assertRaises(SystemExit) as custom_exception:
            self.instance = ProcessInputFile(self.input_filepath_invalid)
        self.assertEqual(custom_exception.exception.code,128)

    def test_validate_input_contains_essential_entries(self):
        # incomplete_data_set that each entry misses:
        # - currency
        # - date
        # - lines
        incomplete_data_set=[
            {"invoice":{"date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{'currency':'NZD',"lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{'currency':'NZD',"date":"2020-07-07"}}
        ]
        for test_data in incomplete_data_set:
            with self.assertRaises(SystemExit) as custom_exception:
                self.instance = ProcessInputFile(self.input_filepath)
                self.instance.input_data=test_data
                self.instance._validate_input_keys()
            self.assertEqual(custom_exception.exception.code,2)

    def test_input_date_format_should_conform_rfc3339(self):
        data_with_invalid_date_format=[
            {"invoice":{"currency":"NZD","date":"07-07-2020","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{"currency":"NZD","date":"20201212","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        ]

        for test_data in data_with_invalid_date_format:
            with self.assertRaises(SystemExit) as custom_exception:
                self.instance = ProcessInputFile(self.input_filepath)
                self.instance.input_data=test_data
                self.instance._validate_date()
            self.assertEqual(custom_exception.exception.code,3)

    def test_input_currency_should_conform_iso4217(self):
        date_with_invalid_currency=[
            {"invoice":{"currency":"ABC","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{"currency":"CDE","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        ]
        for test_data in date_with_invalid_currency:
            with self.assertRaises(SystemExit) as custom_exception:
                self.instance = ProcessInputFile(self.input_filepath)
                self.instance.input_data=test_data
                self.instance._validate_currency()
            self.assertEqual(custom_exception.exception.code,4)

    def test_input_invoice_lines_essential_keys_should_exist(self):
        date_with_missing_keys_in_lines=[
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"currency":"USD","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"USD"},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        ]
        for test_data in date_with_missing_keys_in_lines:
            with self.assertRaises(SystemExit) as custom_exception:
                self.instance = ProcessInputFile(self.input_filepath)
                self.instance.input_data=test_data
                self.instance._validate_input_invoice_lines_key_exist()
            self.assertEqual(custom_exception.exception.code,5)

    def test_input_invoice_lines_currency_should_valid(self):
        date_with_invalid_line_currency=[
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"ABC","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"CDE","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}},
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"FGH","amount":700},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        ]
        for test_data in date_with_invalid_line_currency:
            with self.assertRaises(SystemExit) as custom_exception:
                self.instance = ProcessInputFile(self.input_filepath)
                self.instance.input_data=test_data
                self.instance._validate_input_invoice_lines_currency_valid()
            self.assertEqual(custom_exception.exception.code,6)

    def test_input_invoice_lines_amount_less_than_two_decimals(self):
        date_with_invalid_amount_decimal=[
            {"invoice":{"currency":"NZD","date":"2020-07-07","lines":[{"description":"Intel Core i9","currency":"AUD","amount":700.123},{"description":"ASUS ROG Strix","currency":"AUD","amount":500}]}}
        ]
        for test_data in date_with_invalid_amount_decimal:
            with self.assertRaises(SystemExit) as custom_exception:
                self.instance = ProcessInputFile(self.input_filepath)
                self.instance.input_data=test_data
                self.instance._validate_input_invoice_lines_amount()
            self.assertEqual(custom_exception.exception.code,7)
