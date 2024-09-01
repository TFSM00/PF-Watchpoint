import streamlit as st
from wp.column_configs import EXPENSES_COLUMN_CONFIG
from wp.managers.watchpoint_manager import ExpensesManager, WatchPointManager
from wp.startup import startup

startup()

expenses = ExpensesManager.loadExpenses()
st.header('Expenses')
# if st.button('Refresh'):
#     expenses = getExpenses()

header_col1, header_col2 = st.columns(2)
data_view = header_col2.selectbox('Data', options=('Read', 'Write'))

if header_col1.button('Refresh'):
    expenses = ExpensesManager.loadExpenses()

if header_col1.button('Save'):
    edited_df = WatchPointManager.getEditedDF(expenses, st.session_state['expense_data'])
    ExpensesManager.saveExpenses(edited_df)

edited_data = st.data_editor(expenses,
                hide_index=True,
                width=4000,
                column_config=EXPENSES_COLUMN_CONFIG,
                disabled=(data_view != 'Write'),
                key='expense_data',
                num_rows='dynamic' if data_view == 'Write' else 'fixed')

