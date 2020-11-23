# multi-currency invoice program

This program loads in input data files containing lines of invoice, then outputs
total invoice amount in desired currency.

## input data sample

```json
{
  "invoice": {
    "currency": "NZD",
    "date": "2020-07-07",
    "lines": [
      {
        "description": "Intel Core i9",
        "currency": "USD",
        "amount": 700
      },
      {
        "description": "ASUS ROG Strix",
        "currency": "AUD",
        "amount": 500
      }
    ]
  }
}
```