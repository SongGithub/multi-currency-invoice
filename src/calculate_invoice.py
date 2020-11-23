
class Invoice(object):

    def __init__(self, input_data):
        self.base_currency = input_data['invoice']['currency']
        self.lines = input_data['invoice']['lines']
        self.invoice_total = 0
        # cache result for exchangeRate, because it is an expensive operation to fetch data from API.
        self.currency_cache = {'AUD':123}

    def retrieve_exchangerate_from_api(self,requesting_curr_list):
        """
            inputs:
                - target currency([str])
                - base currency(str)
                - date
            output: updates to self.currency_cache(dict) (round to 4 decimal)

        """
        pass

    def generate_request_items(self):
        """

        """
        requesting_curr_list = []
        for line in self.lines:
            if line['currency'] != self.base_currency and line['currency'] not in self.currency_cache:
                requesting_curr_list.append(line['currency'])
        return requesting_curr_list


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
        print(str(sum(line_totals)),'\n')