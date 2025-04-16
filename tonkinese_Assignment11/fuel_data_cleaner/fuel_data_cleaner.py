#fuel_data_cleaner.py
#Name: Tonkinese - Alisha Siddiqui and Leah Radcliffe
#email: siddiqas@mail.uc.edu and radclilr@mail.uc.edu
#Assignment Number:Assignment 11
#Due Date: 04/17/2025
#Course/Section: IS
#Semester/Year: Spring 2025
#Brief description of mmodule: This module involves data cleaning and then the clean data and 
# the outliers are saved to specified files, with a completion message confirming the process.
#Citations: zipcodebase.com 
import csv
import os
import requests
from decimal import Decimal, ROUND_HALF_UP

class FuelDataCleaner:
    def __init__(self, input_file, cleaned_file, anomaly_file, api_key=None):
        self.input_file = input_file
        self.cleaned_file = cleaned_file
        self.anomaly_file = anomaly_file
        self.api_key = api_key
        self.rows_seen = set()
        self.api_lookups_done = 0
        self.max_api_lookups = 5
        self.zipcode_api_url = "https://app.zipcodebase.com/api/v1/search"

    def round_price(self, price):
        try:
            return str(Decimal(price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        except:
            return price

    def get_zip_code(self, city):
        if self.api_lookups_done >= self.max_api_lookups or not self.api_key:
            return "00000"

        params = {
            'apikey': self.api_key,
            'city': city,
            'country': 'US'
        }
        try:
            response = requests.get(self.zipcode_api_url, params=params)
            data = response.json()
            if 'results' in data and city in data['results']:
                print(f"API Lookup #{self.api_lookups_done + 1}: {city}")
                self.api_lookups_done += 1
                return data['results'][city][0]['postal_code']
        except:
            pass
        return "00000"

    def clean_data(self):
        with open(self.input_file, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames

            os.makedirs(os.path.dirname(self.cleaned_file), exist_ok=True)
            os.makedirs(os.path.dirname(self.anomaly_file), exist_ok=True)

            with open(self.cleaned_file, 'w', newline='', encoding='utf-8') as clean_out, \
                 open(self.anomaly_file, 'w', newline='', encoding='utf-8') as anomaly_out:

                clean_writer = csv.DictWriter(clean_out, fieldnames=fieldnames)
                anomaly_writer = csv.DictWriter(anomaly_out, fieldnames=fieldnames)

                clean_writer.writeheader()
                anomaly_writer.writeheader()

                for row in reader:
                    row_tuple = tuple(row.items())
                    if row_tuple in self.rows_seen:
                        continue
                    self.rows_seen.add(row_tuple)

                    if row.get('Fuel Type', '').lower() == 'pepsi':
                        anomaly_writer.writerow(row)
                        continue

                    row['Gross Price'] = self.round_price(row.get('Gross Price', row.get('gross price', '')))

                    if (row.get('Zip Code', '') == '' or row.get('Zip Code') is None) and row.get('City'):
                        row['Zip Code'] = self.get_zip_code(row.get('City'))

                    clean_writer.writerow(row)
