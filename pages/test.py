import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
from wp.managers.expense_manager import ExpensesManager
from tests.extract_load import Extractors
import pandas as pd

df = ExpensesManager.loadExpenses()
from wp.pages import menu

menu()
# new_dfs, code = spreadsheet(df)

# if st.button('Save'):
#     st.write(new_dfs['df1'])

# if st.button('Clear'):
#     al = None

def file_upload_status_setting(account, parser):
    '''
    Receives the account name and the appropriate extractor function.\n
    Gets the file path \n
    Try to parse the file \n
    If it cannot, pass the error to the error code
    '''
    file = st.session_state.get(f'path_{account}', None)
    
    try:
        if file is not None:
            data = parser(file)
            st.session_state[f'file_upload_{account}_status'] = ['complete', 'Data loading successful']
            st.session_state[f'data_{account}'] = data
        else:
            st.session_state[f'file_upload_{account}_status'] = ['warning', 'No data loaded']
    except Exception as e:
        st.session_state[f'file_upload_{account}_status'] = ['error', f'Error loading data: {e}']

st.header('Update Files')
st.divider()

# Accounts attribute is a dict with the account name and the appropriate method to extract the data
for account, parser in Extractors.accounts.items():
    container = st.expander(f'##### Statement for {account}', expanded=True)

    # Add a default status of no data loaded for the first run
    if f'file_upload_{account}_status' not in st.session_state:
        st.session_state[f'file_upload_{account}_status'] = ['warning', 'No data loaded']

    # TODO: Try success error bubble instead of status
    status = st.session_state[f'file_upload_{account}_status']

    # On change function added to dynamically adjust the 'status'
    file_upload_widget = container.file_uploader(
        label=f'{account}',
        key=f'path_{account}',
        on_change=file_upload_status_setting,
        args=(account, parser,)
    )

    # Appropriately change the status bar to the one according to the error codes
    if status[0] == 'complete':
        container.success(status[1])
    elif status[0] == 'error':
        container.error(status[1])
    else:
        container.warning(status[1])

if st.button('Merge', 'merger'):
    st.session_state['file_upload_data'] = {
        account: st.session_state[f'path_{account}']
        for account in Extractors.accounts
    }  

    st.switch_page('pages/merger.py')

