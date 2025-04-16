from fuel_data_cleaner.fuel_data_cleaner import FuelDataCleaner

if __name__ == '__main__':
    api_key = "f441e640-1af9-11f0-ae0e-6f12e880608e"

    cleaner = FuelDataCleaner(
        input_file='data/fuelPurchaseData.csv',
        cleaned_file='data/cleanedData.csv',
        anomaly_file='data/dataAnomalies.csv',
        api_key=api_key
    )

    cleaner.clean_data()
    print("Data cleanup complete.")
