import streamlit as st
from wp.column_configs import EXPENSES_COLUMN_CONFIG
from wp.managers.watchpoint_manager import ExpensesManager, WatchPointManager
from wp.startup import startup

startup()

expenses = ExpensesManager.loadExpenses()
st.header('Expenses')

edited_data = st.dataframe(expenses,
                hide_index=True,
                width=4000,
                column_config=EXPENSES_COLUMN_CONFIG)

