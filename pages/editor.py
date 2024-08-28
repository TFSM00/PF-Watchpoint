import streamlit as st
import pandas as pd
from wp.managers.expense_manager import ExpensesManager
from wp.column_configs import DB_TABLE_COL_CFG
from wp.pages import menu
from wp.utils import Utils
menu()

st.header('Data Editor')


db_table_name = st.selectbox(
    label='Select database table',
    options=[type.capitalize() for type in st.session_state['database']]
)

# The names are capitalized to look better for the user. Then I lower the string for data handling purposes

db_table = st.session_state['database'][db_table_name.lower()]

data = st.data_editor(db_table,
                      hide_index=True,
                      column_config=DB_TABLE_COL_CFG[db_table_name.lower()],
                      use_container_width=True)

if st.button('Save'):
    Utils.data_savers[db_table_name.lower()](data)
    Utils.update_db(db_table_name.lower(), data)