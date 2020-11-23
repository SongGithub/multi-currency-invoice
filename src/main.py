#!/usr/bin/env python

import sys

from process_input import ProcessInputFile
from calculate_invoice import Invoice

def main():
    if len(sys.argv) != 2:
        print('Error: expect a single input file per run, but either none was found, or more than one argument present \n')
        sys.exit(1)
    json_instance = ProcessInputFile(sys.argv[1])
    json_instance.validate_input()
    validated_input_data = json_instance.input_data

    invoice_instance = Invoice(validated_input_data)
    invoice_instance.prepare_currency_cache()
    print(invoice_instance.calculate_invoice_total(),'\n')

if __name__ == '__main__':
    main()
