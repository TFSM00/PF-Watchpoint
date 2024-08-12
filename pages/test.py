import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from wp.managers.expense_manager import ExpensesManager
import pandas as pd

df = ExpensesManager.loadExpenses()

new_dfs, code = spreadsheet(df)

if st.button('Save'):
    st.write(new_dfs['df1'])

if st.button('Clear'):
    al = None

