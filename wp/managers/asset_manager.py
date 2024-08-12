import openpyxl as xl
import pandas as pd
import datetime as dt
import numpy as np

class AssetManager:
    @staticmethod
    def getSheetNames():
        """Gets all the sheet names within the assets file

        Returns:
            list
        """
        wb = xl.load_workbook(filename='data/assets.xlsx')
        return wb.sheetnames
    
    @staticmethod
    def getSheet(sheet_name: str):
        """Gets a dataframe from a sheet in the assets file

        Args:
            sheet_name (str): sheet name from assets file

        Returns:
            pd.DataFrame: excel file as a dataframe
        """
        with pd.ExcelFile('data/assets.xlsx') as assets:
            data = pd.read_excel(assets, sheet_name)
            data['date'] = pd.to_datetime(data['date'], format="%d/%m/%Y")
            return data
        
    @staticmethod
    def getAllSheets():
        """Gets all sheets as dataframes

        Returns:
            list: list of dataframes within the assets file
        """

        sheet_dfs = []
        for sheet in AssetManager.getSheetNames():
            sheet_dfs.append(AssetManager.getSheet(sheet))
        return sheet_dfs
    
    @staticmethod
    def saveSheet(sheet_name: str, data: pd.DataFrame):
        """Saves the data from the dataframes to excel

        Args:
            sheet_name (str): name of the excel sheet
            data (pd.DataFrame): sheet data in dataframe form
        """
        
        with pd.ExcelWriter('data/assets.xlsx', mode="a", if_sheet_exists='replace') as writer:
            data.to_excel(writer, sheet_name=sheet_name, index=False)
   
    @staticmethod
    def updateBalance(savings_account_name: str):
        today = dt.datetime.now()
        deposits = AssetManager.getSheet('Deposits')
        deposits.loc[deposits['name'] == savings_account_name, 'nominal'] = np.int64(WatchPointManager.getBalanceData()['balance'])
        deposits.loc[deposits['name'] == savings_account_name, 'date'] = today
        AssetManager.saveSheet('Deposits', deposits)