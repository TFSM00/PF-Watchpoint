import streamlit as st
from wp.pages import menu
from tests.extract_load import Extractors
from tests.merge import merge_data
menu()

file_upload_data = st.session_state.get('file_upload_data', None)

#dataframes = [Extractors.accounts[account](file_upload_data[account]) for account in file_upload_data if file_upload_data[account] is not None]

st.write(merge_data(file_upload_data))

# TODO: HANDLE WIDGETS LOSING THEIR VALUE BETWEEN PAGES