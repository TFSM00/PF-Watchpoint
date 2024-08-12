import pandas as pd
import datetime as dt
import openpyxl as xl
import json

class ExpensesManager:
    @staticmethod
    def loadExpenses():
        with pd.ExcelFile('data/expenses.xlsx') as expenses:
            data = pd.read_excel(expenses, '2024')
            data = data.sort_values(by='date', ascending=False)
            data['date'] = pd.to_datetime(data['date'], format="%d/%m/%Y")
            data['value_date'] = pd.to_datetime(data['value_date'], format="%d/%m/%Y")
            return data
    
    
    @staticmethod
    def saveExpenses(edited_df):
        today = dt.datetime.now()

        with pd.ExcelWriter('data/expenses.xlsx', mode="a", if_sheet_exists='replace') as writer:
            edited_df.to_excel(writer, index=False)

