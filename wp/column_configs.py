import streamlit as st

EXPENSES_COLUMN_CONFIG = {
                   'date': st.column_config.DateColumn(
                       label='Date',
                       format='DD-MM-YYYY'
                   ),
                   'value_date': st.column_config.DateColumn(
                       label='Value Date',
                       format='DD-MM-YYYY'
                   ),
                   'description': st.column_config.Column(
                       label='Description'
                   ),
                   'category': st.column_config.Column(
                       label='Category'
                   ),
                   'nominal': st.column_config.NumberColumn(
                       label='Nominal',
                       format='€ %.2f'
                   ),
                   'balance': st.column_config.NumberColumn(
                       label='Balance',
                       format='€ %.2f'
                   )}

DEPOSITS_COLUMN_CONFIG = {
                   'name': st.column_config.Column(
                       label='Name'
                   ),
                   'nominal': st.column_config.NumberColumn(
                       label='Nominal',
                       format='€ %.2f'
                   ),
                   'currency': st.column_config.Column(
                       label='Currency'
                   ),
                   'institution': st.column_config.Column(
                       label='Institution'
                   ),
                   'yield': st.column_config.NumberColumn(
                       label='Yield',
                       format='%.2g'
                   ),
                   'date': st.column_config.DateColumn(
                       label='Date',
                       format='DD-MM-YYYY'
                   ),
                   'creation_date': st.column_config.DateColumn(
                       label='Creation Date',
                       format='DD-MM-YYYY'
                   ),
                   'description': st.column_config.Column(
                       label='Description'
                   ),
                   'monthly_contribution': st.column_config.NumberColumn(
                       label='Contribution',
                       format='€ %.2f'
                   ),
                   'contributor': st.column_config.Column(
                       label='Contributor'
                   )}

CRYPTO_COLUMN_CONFIG = {
                   'name': st.column_config.Column(
                       label='Name'
                   ),
                   'ticker': st.column_config.Column(
                       label='Ticker'
                   ),
                   'average_cost': st.column_config.NumberColumn(
                       label='Avg. Cost',
                       format='€ %.2f'
                   ),
                   'units': st.column_config.NumberColumn(
                       label='Units',
                       format='%.5f'
                   ),
                   'latest_price': st.column_config.NumberColumn(
                       label='Latest Price',
                       format='€ %.5f'
                   ),
                   'currency': st.column_config.Column(
                       label='Currency'
                   ),
                   'institution': st.column_config.Column(
                       label='Institution'
                   ),
                   'date': st.column_config.DateColumn(
                       label='Last Updated',
                       format='DD-MM-YYYY'
                   ),
                   'value_date': st.column_config.DateColumn(
                       label='Value Date',
                       format='DD-MM-YYYY'
                   )}
