import pandas as pd

class Extractors:
    @staticmethod
    def santander(path: str) -> pd.DataFrame: 
        data = pd.read_excel(path)

        # Handle the top rows that are just information
        data = data[6:]
        data = data.reset_index(drop=True)

        data['category'] = None
        # Add new column names
        data.columns = ["date", "value_date", "description", "amount", "category"]


        # Coerce dates into datetime
        data["date"] = pd.to_datetime(data['date'], dayfirst=True)
        data["value_date"] = pd.to_datetime(data['value_date'], dayfirst=True)

        # Clean amount column and coerce to float
        data['amount'] = data["amount"].apply(lambda x: x.split(' EUR')[0].replace(',', '.'))
        data['amount'] = pd.to_numeric(data['amount']).round(2)

        # Sort to oldest first
        data.sort_values('date', ascending=True, inplace=True)

        # Add balance
        data['balance'] = data['amount'].cumsum().round(2)

        return data

    @staticmethod
    def novo_banco(path: str) -> pd.DataFrame:
        
        try:
            data = pd.read_excel(path)
        except ValueError:
        #   st.warning('Excel provided not in appropriate format.')
            raise ValueError('Excel provided not in appropriate format.')

        # Handle the top rows that are just information
        data.columns = data.loc[8].values
        data = data[9:]
        data = data.reset_index(drop=True)

        data['Débito'] = data["Débito"].apply(lambda x: x.replace('-', '0') if type(x) not in (float, int) else x)
        data['Crédito'] = data['Crédito'].apply(lambda x: x.replace('-', '0') if type(x) not in (float, int) else x)

        data['Débito'] = pd.to_numeric(data["Débito"])
        data['Crédito'] = pd.to_numeric(data["Crédito"])

        data['amount'] = data['Débito'] + data['Crédito']
        data = data.drop(columns=['Tipo', 'Débito','Crédito'])

        data['category'] = None

        data.columns = ['date', 'value_date', 'description', 'balance', 'amount', 'category']

        data['date'] = pd.to_datetime(data['date'])
        data['value_date'] = pd.to_datetime(data['value_date'])

        data['balance'] = pd.to_numeric(data['balance']).round(2)
        data['amount'] = pd.to_numeric(data['amount']).round(2)
        
        return data
    
    @staticmethod
    def xtb(path: str) -> pd.DataFrame:
        
        try:
            data = pd.read_excel(path, sheet_name = 'CASH OPERATION HISTORY')
        except ValueError:
        #   st.warning('Excel provided not in appropriate format.')
            raise ValueError('Excel provided not in appropriate format.')
        
        # Handle the top rows that are just information
        data.columns = data.loc[9].values
        data = data[10:]
        data = data.reset_index(drop=True)

        # Add balance column
        data['balance'] = None

        # Clean empty columns and rename
        data.columns = ['delete1', 'delete2', 'category', 'date', 'description', 'symbol', 'amount', 'delete3', 'balance']
        for col in data.columns:
            if 'delete' in col:
                del data[col]

        # Data Type Coercions
        data['date'] = pd.to_datetime(data['date'])
        data['amount'] = pd.to_numeric(data['amount']).round(2)

        # Add the balance to the data
        balance = data.loc[len(data) - 1]['amount']
        data.drop(index=(len(data) - 1), inplace=True)
        data.at[len(data) - 1, 'balance'] = balance

        # Populate balance
        for i in range((len(data)-1) - 1, -1, -1):
            data.loc[i, 'balance'] = data.loc[i + 1, 'balance'] + (data.loc[i + 1, 'amount'] * -1)

        for i in range(len(data)):
            if not pd.isna(data.loc[i, 'symbol']):
                data.loc[i, 'description'] = data.loc[i, 'description'] + " - " + data.loc[i, 'symbol']

        del data['symbol']
        data['balance'] = pd.to_numeric(data['balance']).round(2)

        return data
    
    #TODO: Documentation - ADD ACCOUNTS HERE WHEN ENTERING A NEW ACCOUNT
    accounts = {
        "Santander": 
            {'loader': santander,
             'info': 'Data needs to be loaded from first transaction'
            },
        "Novo Banco":
            {'loader': novo_banco,
             'info': 'Data needs to be converted to xlsx'
            },
        "XTB":
            {'loader': xtb,
             'info': ''
            } 
    }

if __name__ == '__main__':
    data = Extractors.santander('santander.xls')
    print(data.dtypes)
    #print(Extractors.accounts["XTB"]())