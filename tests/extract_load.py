import pandas as pd

class Extractors:
    @classmethod
    def extract_santander(path: str) -> pd.DataFrame: 
        with pd.ExcelFile(path) as xl:
            data = pd.read_excel(xl)

            # Handle the top rows that are just information
            data = data[6:]
            data = data.reset_index(drop=True)

            # Add new column names
            data.columns = ["date", "value_date", "description", "amount"]


            # Coerce dates into datetime
            data["date"] = pd.to_datetime(data['date'], format="%d-%m-%Y")
            data["value_date"] = pd.to_datetime(data['value_date'], format="%d-%m-%Y")

            # Clean amount column and coerce to float
            data['amount'] = data["amount"].apply(lambda x: x.split(' EUR')[0].replace(',', '.'))
            data['amount'] = pd.to_numeric(data['amount'])


