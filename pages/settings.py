import streamlit as st
from wp.managers.settings_manager import SettingsManager
from wp.pages import menu

menu()

st.header('Settings')

st.subheader('Load user data')

save_data_tab, load_data_tab = st.tabs(['Save User Data', "Load User Data"])


with save_data_tab:
    if 'user_data' in st.session_state:
        data = st.session_state['user_data']
    else:
        data = {}


    with st.form('user_data_form'):
        account_num = st.number_input('Number of Accounts:', min_value=1, step=1)

        for i in range(account_num):
            st.text_input(f'Account {i} name:')





with load_data_tab:
    if st.button('Load data'):
        user_data = SettingsManager.load_settings('user_data.json')
        st.session_state['user_data'] = user_data



