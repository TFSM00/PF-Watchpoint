import streamlit as st
from wp.managers import ExpensesManager, WatchPointManager, AssetManager, NetWorthAnalyzer
import datetime as dt

import plotly.graph_objects as go
from wp.pages import menu

menu()

#TODO: Load data only once and refresh on-demand
balance, month_expenses, nw = st.columns(3)
balance_data = WatchPointManager.getBalanceData()
balance.metric('Balance', f"€ {balance_data['balance']:.2f}", balance_data['delta'])
balance.caption(f'Last updated on {balance_data["last_updated"].strftime('%d-%m-%Y')}')

expense_data = WatchPointManager.getExpensesData()
month_expenses.metric('Expenses', f"€ {expense_data['expenses']:.2f}", expense_data['delta'], delta_color='inverse')
month_expenses.caption(f'Last updated on {expense_data["last_updated"].strftime('%d-%m-%Y')}')

networth = WatchPointManager.getNetWorth()
nw.metric('Net Worth', f"€ {networth:.2f}")

WatchPointManager.addNetWorthRecord(dt.datetime.now(), balance_data['balance'], expense_data['expenses'], networth)
nw_data = WatchPointManager.loadNetWorthDF()
#st.dataframe(WatchPointManager.loadNetWorthDF(), hide_index=True)

# with pd.ExcelWriter('data/nw_data.xlsx', mode="a", if_sheet_exists='replace') as writer:
#     nw_data.to_excel(writer, sheet_name="data", index=False)

st.write('Net Worth Metrics')
st.write(f"{NetWorthAnalyzer.getNetworthMetrics()}")

nw_metrics = NetWorthAnalyzer.getNetworthMetrics()

dod_display, mom_display, yoy_display, ttd_display = st.columns(4)

dod_display.metric('Today', f"{nw_metrics['DoD'][1] * 100:.2f}%",
                        delta=nw_metrics['DoD'][0])
mom_display.metric('Month-on-Month', f"{nw_metrics['MoM'][1] * 100:.2f}%",
                        delta=nw_metrics['MoM'][0])
yoy_display.metric('Year-on-Year', f"{nw_metrics['YoY'][1] * 100:.2f}%",
                        delta=nw_metrics['YoY'][0])
ttd_display.metric('Time-to-Date', f"{nw_metrics['TtD'][1] * 100:.2f}%",
                        delta=nw_metrics['TtD'][0])


fig = go.Figure(
    data=[
        go.Scatter(
            x=nw_data['date'], y=nw_data['net_worth'],
            mode="lines", line = go.scatter.Line(color="#3cd1c2", shape='spline')
        ),
        go.Scatter(
            x=nw_data['date'], y=nw_data['balance'],
            mode="lines", line = go.scatter.Line(color="#e2ba04", shape='spline')
        )
    ]
)


#st.plotly_chart(fig, theme="streamlit", use_container_width=True)
