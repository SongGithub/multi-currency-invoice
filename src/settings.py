"""
This file holds settings for the project
"""
import sys, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SOURCE_DIR = os.path.join(BASE_DIR,'src')
TEST_DIR = os.path.join(BASE_DIR,'tests')
TEST_FIXTURE_ITEM = os.path.join(TEST_DIR,'fixtures','01-input.txt')

EXCHANGE_RATES_API_URL = 'https://api.exchangeratesapi.io'
REQUEST_TIMEOUT = 1