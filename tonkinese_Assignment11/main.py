#main.py
#Name: Tonkinese - Alisha Siddiqui and Leah Radcliffe
#email: siddiqas@mail.uc.edu and radclilr@mail.uc.edu
#Assignment Number:Assignment 11
#Due Date: 04/17/2025
#Course/Section: IS
#Semester/Year: Spring 2025
#Brief description of mmodule: This module involves data cleaning and then the clean data and 
# the outliers are saved to specified files, with a completion message confirming the process.
#Citations: zipcodebase.com 


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
