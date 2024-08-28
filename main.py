import streamlit as st
from wp.managers.watchpoint_manager import WatchPointManager
from wp.managers.networth_analyzer import NetWorthAnalyzer
import datetime as dt
from wp.utils import Utils

import plotly.graph_objects as go
from wp.pages import menu

menu()
Utils.init_db()

#TODO: Load data only once and refresh on-demand
balance, month_expenses, nw = st.columns(3)
balance_data = WatchPointManager.getBalanceData()
balance.metric('Balance', f"€ {balance_data['balance']:.2f}", balance_data['delta'])
balance.caption(f"Last updated on {balance_data['last_updated'].strftime('%d-%m-%Y')}")

expense_data = WatchPointManager.getExpensesData()
month_expenses.metric('Expenses', f"€ {expense_data['expenses']:.2f}", expense_data['delta'], delta_color='inverse')
month_expenses.caption(f"Last updated on {expense_data['last_updated'].strftime('%d-%m-%Y')}")

networth = WatchPointManager.getNetWorth()
nw.metric('Net Worth', f"€ {networth:.2f}")
