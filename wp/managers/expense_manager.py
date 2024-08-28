import pandas as pd
import os

class ExpensesManager:
    @staticmethod
    def loadExpenses() -> pd.DataFrame | None:
        if 'expenses.csv' not in os.listdir('data/'):
            return None
        
        df = pd.read_csv('data/expenses.csv')
        df['date'] = pd.to_datetime(df['date'])
        df['value_date'] = pd.to_datetime(df['value_date'])
        df = df.round({'amount': 2, 'account_balance': 2})

        return df 

    
    @staticmethod
    def saveExpenses(edited_df: pd.DataFrame) -> None:
        edited_df.to_csv('data/expenses.csv', index=False)

    @staticmethod
    def mergeExpenses(expenses_df: pd.DataFrame, extract_df: pd.DataFrame) -> pd.DataFrame:
        merged_df = pd.concat([expenses_df, extract_df])

        merged_df['date'] = pd.to_datetime(merged_df['date'])
        merged_df['value_date'] = pd.to_datetime(merged_df['value_date'])

        # Handle duplicates
        merged_df.drop_duplicates(
            subset=['date', 'account', 'amount', 'account_balance'],
            keep='last',
            inplace=True
        )

        merged_df.reset_index(drop=True, inplace=True)
        # Handle duplicates manually? Show all duplicates and allow selection?
        


        return merged_df
    

