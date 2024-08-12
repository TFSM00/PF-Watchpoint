import pandas as pd
import datetime as dt
import numpy as np
import calendar
from wp.managers.expense_manager import ExpensesManager
from wp.managers.asset_manager import AssetManager

class WatchPointManager:
    @staticmethod
    def getEditedDF(base_df, ss_editor_key):
        edited_rows = ss_editor_key['edited_rows']
        added_rows = ss_editor_key['added_rows']
        deleted_rows = ss_editor_key['deleted_rows']

        for row_idx, changes in edited_rows.items():
            for col, new_value in changes.items():
                base_df.at[row_idx, col] = new_value

        # Step 2: Add new rows
        if added_rows:
            new_df = pd.DataFrame(added_rows)
            base_df = pd.concat([base_df, new_df], ignore_index=True)

        # Step 3: Delete rows
        base_df.drop(index=deleted_rows, inplace=True)

        # Reindex the DataFrame after deleting rows to maintain continuous indices
        base_df.reset_index(drop=True, inplace=True)
        return base_df
    
    @staticmethod
    def getMonthName(month: int) -> str | None:
        if month > 0 and month <= 12:
            return str.capitalize(calendar.Month(month).name)
        else:
            return None
        
    @staticmethod
    def getMonthNumber(month: str) -> int:
        return getattr(calendar, month.upper())
    
    @staticmethod
    def getNetWorth():
        net_worth = 0
        for df in AssetManager.getAllSheets():
            if 'nominal' in df:
                net_worth += df['nominal'].sum()
            if 'units' in df:
                value = df['units'] * df['latest_price']
                net_worth += value.sum()
        return net_worth
    
    @staticmethod
    def getExpensesData():
        today = dt.datetime.now()
        df = ExpensesManager.loadExpenses()
        
        month_expenses = df.loc[(df['date'] >= np.datetime64(dt.date(today.year, today.month, 1))) & (df['nominal'] <= 0)]
        previous_month_year = today.year if today.month - 1 != 0 else today.year - 1
        previous_month_month = today.month - 1 if today.month != 1 else 12
        days_in_previous_month = calendar.monthrange(previous_month_year, previous_month_month)[1]
        previous_month_day = today.day if days_in_previous_month > today.day else days_in_previous_month

        
        last_month_expenses_match = df.loc[(df['date'] >= np.datetime64(dt.date(previous_month_year, previous_month_month, previous_month_day))) & (df['nominal'] <= 0)]
        month_expenses_match = df.loc[(df['date'] >= np.datetime64(today)) & (df['nominal'] <= 0)]

        if len(month_expenses) == 0:
            month_expenses = df.sort_values('date')
            
        data = {
            "expenses": round(month_expenses['nominal'].sum(), 2),
            "delta": round(last_month_expenses_match['nominal'].sum() - month_expenses_match['nominal'].sum(), 2),
            "last_updated": month_expenses.iloc[0].date
        }
        return data
    

    @staticmethod
    def getBalanceData():
        today = dt.datetime.now()
        df = ExpensesManager.loadExpenses()
        month_expenses = df.loc[df['date'] >= f"{today.year}-{today.month}-01"]

        # If there are no rows of the current month
        if len(month_expenses) == 0:
            month_expenses = df.sort_values('date')

        data = {
            "balance": df['balance'].iloc[0],
            "initial_balance": month_expenses.iloc[0].balance,
            "delta": round(month_expenses['nominal'].sum(), 2),
            "last_updated": month_expenses.iloc[0].date
        }
        return data
    



    




            
