import streamlit as st
st.set_page_config(layout="wide")

def menu():

    st.sidebar.write('PFWatchpoint')
    with st.sidebar.expander('Assets'):
        st.page_link('pages/assets.py', label="Assets Table")
    with st.sidebar.expander('Expenses'):
        st.page_link('pages/expenses.py', label="Expenses Table")
        st.page_link('pages/expense_analysis.py', label="Expense Analysis")
    with st.sidebar.expander('Savings'):
        st.page_link('pages/emergency.py', label='Emergency Fund')
    #st.sidebar.page_link('pages/settings.py', label='Settings')
    #st.sidebar.page_link('pages/merger.py', label='Merger')
    st.sidebar.page_link('pages/loader.py', label='Data Loader')
    st.sidebar.page_link('pages/editor.py', label='Data Editor')