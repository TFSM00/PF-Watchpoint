import streamlit as st
from wp.managers.expense_manager import ExpensesManager
from wp.extractors import Extractors
import pandas as pd

class Utils:
    """
    A series of core functions and variables to handle repetitive activities within PFWatchpoint
    """

    data_savers = {
        'expenses': ExpensesManager.saveExpenses
    }

    @staticmethod
    def init_db() -> None:
        """
        Create a session state data storage by loading the available data files and storing them as variables
        """
        if 'database' not in st.session_state:
            expenses = ExpensesManager.loadExpenses()
            st.session_state['database'] = {
                'expenses': expenses
            }
    
    @staticmethod
    def update_db(type: str, data: pd.DataFrame) -> None:
        """Updates only the session state data storage

        Args:
            type (str): Name of data table in DB
            data (pd.DataFrame): Data table as Dataframe
        """
        st.session_state['database'][type] = data

    def merge_data(account_data: dict) -> pd.DataFrame:
        """Uses the provided dict with account names and path to the extracts. \n
        Adds the account name to each entry. \n
        Concatenates all dfs and handles the empty value dates by copying the date of the transaction.

        Args:
            account_data (dict): Dictionary with account names as keys and path of file as values
        Returns:
            pd.DataFrame: Concatenated result of account dataframes
        """
        dataframes = []
        for account, path in account_data.items():
            if path != None:
                df = Extractors.accounts[account]['loader'](path)

                if 'balance' in df.columns:
                    cols = list(df.columns)
                    idx = cols.index('balance')
                    cols[idx] = 'account_balance'
                    df.columns = cols
                df['account'] = account
                df['account_balance'] = df['account_balance'].astype(float)

                if 'value_date' not in df.columns:
                    df['value_date'] = df['date']

                dataframes.append(df)

        main = pd.concat(dataframes)
        main.reset_index(drop=True, inplace=True)

        main['date'] = pd.to_datetime(main['date'])
        main['value_date'] = pd.to_datetime(main['value_date'])

        main.sort_values('date', ascending=False, inplace=True)
        main.reset_index(drop=True, inplace=True)

        main = main.round({'amount': 2, 'account_balance': 2})

        return main
    
    @staticmethod
    def clear_loader_files():
        for account in Extractors.accounts:
            if f'path_{account}' in st.session_state and f'file_upload_{account}_status' in st.session_state:
                st.session_state[f'path_{account}'] = None
                st.session_state[f'file_upload_{account}_status'] = ['warning', 'No data loaded']

    @staticmethod
    def ensure_dataypes(df):
        for col in df.columns:
            if col in ['account', 'description']:
                df[col] = df[col].astype(str)
            elif col in ['date', 'value_date']:
                df[col] = pd.to_datetime(df[col])
            elif col in ['amount', 'account_balance']:
                df[col] = df[col].astype(float).round(2)

        return df


