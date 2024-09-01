import streamlit as st

from wp.managers.expense_manager import ExpensesManager
from wp.extractors import Extractors
import pandas as pd

df = ExpensesManager.loadExpenses()
from wp.startup import startup

startup()


def file_upload_status_setting(account, parser, file=None):
    '''
    Receives the account name and the appropriate extractor function.\n
    Gets the file path \n
    Try to parse the file \n
    If it cannot, pass the error to the error code
    '''

    try:
        if file is not None:    
            data = parser(file)
            st.session_state[f'file_upload_{account}_status'] = ['complete', 'Data loading successful']
            st.session_state[f'data_{account}'] = data
        else:
            st.session_state[f'file_upload_{account}_status'] = ['warning', 'No data loaded']
    except Exception as e:
        st.session_state[f'file_upload_{account}_status'] = ['error', f'Error loading data: {e}']
    
    return

    

st.header('Update Files')
st.divider()


# Accounts attribute is a dict with the account name and the appropriate method to extract the data
for account, extractor_data in Extractors.accounts.items():
    #file_upload_status_setting(account, parser)
    with st.expander(f'##### Statement for {account}', expanded=True):
        if extractor_data['info']:
            st.info(extractor_data['info'])
        # Add a default status of no data loaded for the first run
        if f'file_upload_{account}_status' not in st.session_state:
            st.session_state[f'file_upload_{account}_status'] = ['warning', 'No data loaded']

        if f'path_{account}' not in st.session_state:
            st.session_state[f'path_{account}'] = None

        # On change function added to dynamically adjust the 'status'
        file_upload_widget = st.file_uploader(
            label=f'{account}',
            on_change=file_upload_status_setting,
            args=(account, extractor_data['loader'],)
        )

        if file_upload_widget is not None:
            st.session_state[f'path_{account}'] = file_upload_widget
            file_upload_status_setting(account, extractor_data['loader'], file_upload_widget)

        # TODO: Try success error bubble instead of status
        status = st.session_state[f'file_upload_{account}_status']


        # Appropriately change the status bar to the one according to the error codes
        if status[0] == 'complete':
            st.success(status[1])
        elif status[0] == 'error':
            st.error(status[1])
        else:
            st.warning(status[1])


if st.button('Merge'):
    data_loaded = False
    for account in Extractors.accounts:
        if f'path_{account}' in st.session_state and st.session_state[f'path_{account}'] != None:
            data_loaded = True
            
    if not data_loaded:
        st.toast('No data loaded! Cannot merge.')
    else:
        st.session_state['file_upload_data'] = {
            account: st.session_state[f'path_{account}']
            for account in Extractors.accounts
        }  

        st.switch_page('pages/merger.py')

