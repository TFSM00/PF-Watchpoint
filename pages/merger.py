import streamlit as st
from wp.pages import menu
from wp.managers.expense_manager import ExpensesManager
from wp.utils import Utils
from wp.column_configs import EXPENSES_COLUMN_CONFIG
import pandas as pd

menu()

st.header('Data Editor')

file_upload_data = st.session_state.get('file_upload_data', None)

new_transactions = Utils.merge_data(file_upload_data)


saved_df = ExpensesManager.loadExpenses()
newest_saved = saved_df['date'].max()
newest_input = new_transactions['date'].max()

new_changes = new_transactions[new_transactions['date'] >= newest_saved]

st.subheader('New Rows')
data = st.data_editor(new_changes,
                      hide_index=True,
                      column_config=EXPENSES_COLUMN_CONFIG,
                      use_container_width=True)


final_df = pd.concat([saved_df, data], ignore_index=True)
# TODO: Older transactions uploaded after newer ones will not be added. CHANGE THIS. create old_changes, concat in this line
final_df.drop_duplicates(
    subset=['date', 'value_date', 'amount', 'account', 'account_balance'],
    keep='first', 
    # Keep first because changed row is last and 
    # we want whatever is already there because it's probably already changed
    inplace=True 
)

st.subheader('Import Result Preview')
st.dataframe(final_df,
             hide_index=True,
             column_config=EXPENSES_COLUMN_CONFIG,
             use_container_width=True)


if st.button('Save'):
    ExpensesManager.saveExpenses(final_df)
    Utils.update_db('expenses', final_df)

