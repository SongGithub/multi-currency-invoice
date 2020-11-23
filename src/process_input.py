"""
    this module handles all file input operations
"""
import json,sys,re
from iso4217 import Currency

class ProcessInputFile(object):
    """ProcessInputFile"""

    def __init__(self, input_filename):
        self._input_filename = input_filename
        self.input_data = None
        self.read_json()

    def read_json(self):
        """read json file content'"""
        try:
            with open(self._input_filename) as f:
                self.input_data = json.load(f)
        except IOError as e:
            print("Error: file not found \n")
            sys.exit(128)

    def validate_input(self):
        self._validate_input_keys()
        self._validate_date()
        self._validate_currency()
        self._validate_input_invoice_lines_key_exist()
        self._validate_input_invoice_lines_currency_valid()
        self._validate_input_invoice_lines_amount()

    def _validate_input_keys(self):
        """ An invoice date and base currency, along with multiple
        invoice lines, in JSON format
        """
        missing_keys = []
        for key in ['currency','date','lines']:
            if key not in self.input_data['invoice']:
                missing_keys.append(key)
        if len(missing_keys) > 0:
            for missing_key in missing_keys:
                print('Error: ',missing_key, 'is missing \n')
            sys.exit(2)

    def _validate_date(self):
        """
            The invoice date will be in the RFC3339 Internet date format e.g. 2020-07-27
        """
        regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])'
        match_rfc3339 = re.compile(regex).match
        date = self.input_data['invoice']['date']
        if match_rfc3339(date) is None:
            print("Error: date format fails to conform RFC3339 standard! \n")
            sys.exit(3)

    def _validate_currency(self):
        """
            The invoice base currency will be in ISO4217 alphabetic code format e.g. NZD
        """
        currency = self.input_data['invoice']['currency']
        try:
            currency_obj = Currency(currency)
        except:
            print('Error: invalid currency code \n')
            sys.exit(4)

    def _validate_input_invoice_lines_key_exist(self):
        """
            Each invoice line should include
            - a description,
            - an decimal amount (to 2 places), and
            - a currency e.g. AUD
        """
        for line in self.input_data['invoice']['lines']:
            for key in ['description','amount','currency']:
                if key not in line:
                    print('Error: ',key, 'is missing \n')
                    sys.exit(5)

    def _validate_input_invoice_lines_currency_valid(self):
        """
            Each invoice line should include a valid currency code
        """
        for line in self.input_data['invoice']['lines']:
            try:
                line_currency = line['currency']
                line_currency_obj = Currency(line_currency)
            except:
                print('Error: invalid currency code in a line \n')
                sys.exit(6)

    def _validate_input_invoice_lines_amount(self):
        """
            Each invoice line should include
            an decimal amount (to 2 places)
        """
        for line in self.input_data['invoice']['lines']:

            line_amount = str(line['amount'])
            if '.' in line_amount and len(line_amount.rsplit('.')[-1]) > 2:
                print('Error: ',line_amount,' contains >2 decimals in amount in a line \n')
                sys.exit(7)

