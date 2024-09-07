import streamlit as st
from wp.managers.watchpoint_manager import WatchPointManager
from wp.managers.expense_manager import ExpensesManager
from wp.managers.networth_analyzer import NetWorthAnalyzer
import datetime as dt
from wp.utils import Utils
from wp.startup import boot, startup

import plotly.graph_objects as go
from wp.pages import menu

boot()
startup()

# #TODO: Load data only once and refresh on-demand
# balance, month_expenses, nw = st.columns(3)
# balance_data = WatchPointManager.getBalanceData()
# balance.metric('Balance', f"€ {balance_data['balance']:.2f}", balance_data['delta'])
# balance.caption(f"Last updated on {balance_data['last_updated'].strftime('%d-%m-%Y')}")

# expense_data = WatchPointManager.getExpensesData()
# month_expenses.metric('Expenses', f"€ {expense_data['expenses']:.2f}", expense_data['delta'], delta_color='inverse')
# month_expenses.caption(f"Last updated on {expense_data['last_updated'].strftime('%d-%m-%Y')}")

# networth = WatchPointManager.getNetWorth()
# nw.metric('Net Worth', f"€ {networth:.2f}")

account_balances = WatchPointManager.getAccountBalances()
expenses = ExpensesManager.loadExpenses()

total_cash = sum(list(account_balances.values()))
total_investments = round(abs(sum(expenses[expenses['category'].str.contains('ETF')]['amount'].tolist())), 2)

st.markdown('# Networth Metrics')

st.metric(
    label='Total Networth',
    value=total_cash + total_investments
)

col1, col2 = st.columns(2)
col1.metric(
    label='Total Cash Balance',
    value=total_cash
)

col2.metric(
    label='Total Investment Value',
    value=total_investments
)

st.markdown('# Account Balances')
account_cols = st.columns(len(account_balances))

for col, account, value in zip(account_cols, list(account_balances.keys()), list(account_balances.values())):
    col.metric(
        label=account,
        value=value
    )


st.markdown('# Expenses')
st.metric('Expenses', f"€ {expenses['expenses']:.2f}", expenses['amount'], delta_color='inverse')
st.caption(f"Last updated on {expenses['last_updated'].strftime('%d-%m-%Y')}")
