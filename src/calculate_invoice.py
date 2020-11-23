import requests,sys
import settings

class Invoice(object):

    def __init__(self, input_data):
        self.base_currency = input_data['invoice']['currency']
        self.invoice_date = input_data['invoice']['date']
        self.lines = input_data['invoice']['lines']
        self.invoice_total = 0
        # cache result for exchangeRate, because it is an expensive operation to fetch data from API.
        self.currency_cache = {}


    def retrieve_exchangerate_from_api(self,requesting_curr_list):
        """
            inputs:
                - target currency([str])
                - base currency(str)
                - date
            output: response in json format

        """
        api_endpoint = settings.EXCHANGE_RATES_API_URL + '/' + self.invoice_date
        headers = {'Content-Type': 'application/json'}
        payload = {}
        payload['base'] = self.base_currency
        payload['symbols'] = ','.join(requesting_curr_list)
        r = requests.get(api_endpoint, payload, headers=headers, timeout=1)
        if r.status_code != 200:
            print('Error: API was not healthy, error code: ', r.status_code, '\n')
            sys.exit(8)

        for currency in requesting_curr_list:
            if not r.json()['rates'][currency] > 0:
                print('Error: response for currency was invalid  (<=0) \n')
                sys.exit(9)
        return r.json()

    def update_currency_cache(self,api_response):
        """
            this method take input from API response, then update exchange-rate cache aka currency_cache, (round to 4 decimal)
        """
        ex_rates = api_response['rates']
        for key in ex_rates.keys():
            print(key)

    def generate_request_items(self):
        """
            prepare the currency_cache with all required exchange-rates.
        """
        requesting_curr_list = []
        for line in self.lines:
            if line['currency'] != self.base_currency and line['currency'] not in self.currency_cache:
                requesting_curr_list.append(line['currency'])
        return requesting_curr_list

    def prepare_currency_cache(self):
        """
            orchestrating the 2 methods from same Class:
            - generate_request_items() &
            - retrieve_exchangerate_from_api()
        """
        requesting_curr_list = self.generate_request_items()
        print('requesting_curr_list is', requesting_curr_list)
        resp = self.retrieve_exchangerate_from_api(requesting_curr_list)
        self.update_currency_cache(resp)

    def get_exchange_rate(self,line):
        line_currency = line['currency']
        return self.currency_cache[line_currency]

    def calculate_line_total(self,line):
        """
            - output: line_total (rounding using Google Sheets ROUND func)
        """
        line_currency = line['currency']
        return line['amount'] / self.get_exchange_rate(line) # TODO: round to 2 with googleSheet method

    def calculate_invoice_total(self):
        """
            - input: input_data
            - output: invoice_total
        """
        line_totals = []
        for line in self.lines:
            line_total = calculate_line_total(line)
            line_totals.append(line_totals)
        # print(str(sum(line_totals)),'\n')