import streamlit as st
from wp.managers.watchpoint_manager import ExpensesManager, AssetManager
from wp.column_configs import DEPOSITS_COLUMN_CONFIG, CRYPTO_COLUMN_CONFIG
from wp.startup import startup

startup()

expenses = ExpensesManager.loadExpenses()

configs = {"Deposits": DEPOSITS_COLUMN_CONFIG,
           "Crypto": CRYPTO_COLUMN_CONFIG,
           "Stocks": CRYPTO_COLUMN_CONFIG}
#AssetManager.updateBalance()

st.header('Assets')

sheet = st.selectbox(label='Select a sheet', options=AssetManager.getSheetNames())

st.dataframe(AssetManager.getSheet(sheet),
             hide_index=True,
             column_config=configs[sheet],
             width=4000)

