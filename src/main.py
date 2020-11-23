#!/usr/bin/env python

import sys,json,os

from process_input import ProcessInputFile
from calculate_invoice import Invoice

def main():

    json_instance = ProcessInputFile(sys.argv[1])
    json_instance.validate_input()
    input_data = json_instance.input_data
    print(input_data)
    invoice_instance = Invoice(input_data)

    print(invoice_instance.prepare_currency_cache())

    print('1600.86'+'\n')
    # if json_data:
    #     # print(json_data)
    #     print('1600.86'+'\n')

if __name__ == '__main__':
    main()
