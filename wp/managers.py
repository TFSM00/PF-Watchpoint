import streamlit as st
import pandas as pd
import datetime as dt
import openpyxl as xl
import numpy as np
import calendar
from dateutil.relativedelta import relativedelta


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
            edited_df.to_excel(writer, sheet_name=f"{today.year}", index=False)
    
class WatchPointManager:
    @staticmethod
    def getEditedDF(base_df, ss_editor_key):
        edited_rows = ss_editor_key['edited_rows']
        for row in edited_rows:
            for col in edited_rows[row]:
                base_df.loc[row, col] = edited_rows[row][col]
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
    def getBalanceData():
        today = dt.datetime.now()
        df = ExpensesManager.loadExpenses()
        month_expenses = df.loc[df['date'] >= f"{today.year}-{today.month}-01"]
        data = {
            "balance": df['balance'].iloc[0],
            "initial_balance": month_expenses.iloc[-1].balance,
            "delta": round(month_expenses['nominal'].sum(), 2),
            "last_updated": month_expenses.iloc[0].date
        }
        return data
    
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
        data = {
            "expenses": round(month_expenses['nominal'].sum(), 2),
            "delta": round(last_month_expenses_match['nominal'].sum() - month_expenses_match['nominal'].sum(), 2),
            "last_updated": month_expenses.iloc[0].date
        }
        return data
    
    def loadNetWorthDF():
        with open('data/nw_data.json', "r") as nw:
            return pd.read_json(nw, orient='split')
        
    def saveNetWorthDF(df: pd.DataFrame):
        with open('data/nw_data.json', "w") as nw:
            df.to_json(nw, orient='split')
        
    def addNetWorthRecord(date, balance, expenses, net_worth):
        df = WatchPointManager.loadNetWorthDF()
        df.loc[len(df)] = [date, balance, expenses, net_worth]
        WatchPointManager.saveNetWorthDF(df)
    
class AssetManager:
    @staticmethod
    def getSheetNames():
        wb = xl.load_workbook(filename='data/assets.xlsx')
        return wb.sheetnames
    
    @staticmethod
    def getSheet(sheet_name: str):
        with pd.ExcelFile('data/assets.xlsx') as assets:
            data = pd.read_excel(assets, sheet_name)
            data['date'] = pd.to_datetime(data['date'], format="%d/%m/%Y")
            return data
        
    @staticmethod
    def getAllSheets():
        sheet_dfs = []
        for sheet in AssetManager.getSheetNames():
            sheet_dfs.append(AssetManager.getSheet(sheet))
        return sheet_dfs
    
    @staticmethod
    def saveSheet(sheet_name: str, data: pd.DataFrame):
        with pd.ExcelWriter('data/assets.xlsx', mode="a", if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=False)
   
    @staticmethod
    def updateBalance():
        today = dt.datetime.now()
        deposits = AssetManager.getSheet('Deposits')
        deposits.loc[deposits['name'] == 'Conta a Ordem NB', 'nominal'] = np.int64(WatchPointManager.getBalanceData()['balance'])
        deposits.loc[deposits['name'] == 'Conta a Ordem NB', 'date'] = today
        AssetManager.saveSheet('Deposits', deposits)

class NetWorthAnalyzer:
    @staticmethod
    def getNetworthMetrics():
        df = WatchPointManager.loadNetWorthDF()
        # Aggregate to get the last reading of each day
        # Assume today is '2024-01-01'
        today = pd.Timestamp.today()

                # Get the last record for today
        today_df = df[df['date'].dt.date == today.date()].tail(1)
        data = {
            "DoD":[None, None],
            "MoM":[None, None],
            "YoY":[None, None],
            "TtD":[None, None]
        }

        if not today_df.empty:
            today_net_worth = today_df.iloc[0]['net_worth']
            
            # Get the last record of the previous day
            previous_day = today - pd.Timedelta(days=1)
            previous_day_df = df[df['date'].dt.date == previous_day.date()].tail(1)
            if not previous_day_df.empty:
                previous_day_net_worth = previous_day_df.iloc[0]['net_worth']
                data['DoD'] = [today_net_worth - previous_day_net_worth,
                    ((today_net_worth - previous_day_net_worth) / previous_day_net_worth) * 100]
            else:
                # Fallback to first record if no previous day data is available
                first_record_net_worth = df.iloc[0]['net_worth']
                data['DoD'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]
            
            # Get the last record of the previous month
            previous_month = today - pd.DateOffset(months=1)
            previous_month_df = df[(df['date'].dt.year == previous_month.year) & (df['date'].dt.month == previous_month.month)].tail(1)
            if not previous_month_df.empty:
                previous_month_net_worth = previous_month_df.iloc[0]['net_worth']
                data['MoM'] = [today_net_worth - previous_month_net_worth,
                    ((today_net_worth - previous_month_net_worth) / previous_month_net_worth) * 100]
            else:
                # Fallback to first record if no previous month data is available
                first_record_net_worth = df.iloc[0]['net_worth']
                data['MoM'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]
            
            # Get the last record of the previous year
            previous_year = today - pd.DateOffset(years=1)
            previous_year_df = df[(df['date'].dt.year == previous_year.year) & (df['date'].dt.month == today.month) & (df['date'].dt.day == today.day)].tail(1)
            if not previous_year_df.empty:
                previous_year_net_worth = previous_year_df.iloc[0]['net_worth']
                data['YoY'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - previous_year_net_worth) / previous_year_net_worth) * 100]
            else:
                # Fallback to first record if no previous year data is available
                first_record_net_worth = df.iloc[0]['net_worth']
                data['YoY'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]
            
            # Calculate all-time growth
            first_record_net_worth = df.iloc[0]['net_worth']
            data['TtD'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]


        return data
    

class DateManager:
    @staticmethod
    def hasSixMonths(dates):
        today = dt.datetime.now()
        return {'rolling_months': min(dates) > (today - relativedelta(months=6)).date(),
                'entire_months':min(dates) > today.replace(day=1, month=((today.month - 6 - 1) % 12 + 1)).date()}

    @staticmethod
    def lastRollingMonthDate(dates):
        today = dt.datetime.now()
        month_diff = today.month - min(dates).month 
        day_diff = today.day - min(dates).day

        if month_diff == 0 or (month_diff == 1 and day_diff < 0):
            return [None, None, 'rolling']
        elif day_diff >= 0:
            return [(today - relativedelta(months=month_diff)).date(), month_diff, 'rolling']
        else:
            return [(today - relativedelta(months=month_diff-1)).date(), month_diff - 1, 'rolling']

    @staticmethod
    def lastEntireMonthDate(dates):
        today = dt.datetime.now()
        first_day = today.replace(day=1)
        if min(dates).day != 1:
            month_diff = first_day.month - (min(dates) + relativedelta(months=1)).month
        else:
            month_diff = first_day.month - min(dates).month

        if month_diff < 1:
            return [None, None, 'entire']
        else:
            return [(first_day - relativedelta(months=month_diff)).date(), month_diff, 'entire']
        


            
