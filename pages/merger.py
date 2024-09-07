import streamlit as st
from wp.managers.expense_manager import ExpensesManager
from wp.utils import Utils
from wp.column_configs import EXPENSES_COLUMN_CONFIG
import pandas as pd

from wp.startup import startup

startup()

st.header('Data Editor')

file_upload_data = st.session_state.get('file_upload_data', None)
new_transactions = Utils.merge_data(file_upload_data).round(2)

saved_df = ExpensesManager.loadExpenses()

if saved_df.empty:
    saved_df = ExpensesManager.loadExpenses().round(2)

merger = pd.concat([saved_df, new_transactions], ignore_index=True)


## Logic for loading duplicates
# We want the new transactions df to be the ones in the new transactions loaded that are not duplicates in
# the saved df following a group of subset columns.
# The following code checks if, comparing the selected columns, the row is already there.
# Duplicates function doesn't work because it would grab rows that are already saved but were not loaded.
# This would show the incorrect result
subset_columns = ['date', 'value_date', 'amount', 'account_balance', 'account']
new_changes = merger[~merger[subset_columns].apply(tuple, 1).isin(saved_df[subset_columns].apply(tuple, 1))]
st.subheader('New Rows - Possible Duplicates')


if not new_changes.empty:
    data = st.data_editor(new_changes,
                      hide_index=True,
                      column_config=EXPENSES_COLUMN_CONFIG,
                      use_container_width=True)
else:
    st.write('No new data loaded.')

final_df = pd.concat([saved_df, new_changes], ignore_index=True)
final_df.sort_values('date', ascending=False, inplace=True)

st.subheader('Import Result Preview')
st.dataframe(final_df,
             hide_index=True,
             column_config=EXPENSES_COLUMN_CONFIG,
             use_container_width=True)

if st.button('Save'):
    ExpensesManager.saveExpenses(final_df)
    Utils.update_db('expenses', final_df)
    Utils.clear_loader_files()

