import streamlit as st
from wp.managers.watchpoint_manager import ExpensesManager, WatchPointManager, DateManager, AssetManager
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wp.startup import startup

startup()

expenses = ExpensesManager.loadExpenses()
accounts = AssetManager.getSheet('Deposits')
today = dt.datetime.now()

# Show emergency fund need for 3,4,6 and 12 months.

dates = expenses['value_date'].dt.date.tolist()
test_dates = expenses.loc[expenses['value_date'] > dt.datetime(2024, 4, 1)]
test_dates =test_dates['value_date'].dt.date.tolist()

rolling_data = DateManager.lastRollingMonthDate(test_dates)
full_month_data =  DateManager.lastEntireMonthDate(test_dates)

is_rolling_window = None
expense_window = None
average_expense = None

info_container = st.empty()

if not rolling_data[0] and not full_month_data[0]:
    st.error('No historical expense data. Enter expected average monthly expenses.')
    average_expense = st.number_input('Enter expected monthly expenses', 0, step=1)
elif rolling_data[0] and not full_month_data[0]:
    st.error('Only rolling data available. Defaulting to rolling window analysis.')
    is_rolling_window = st.checkbox('Apply rolling window?', True, disabled=True)
else:
    rolling_window, account_choice, month_choice = st.columns(3)
    if rolling_data[1]:
        is_rolling_window = rolling_window.checkbox('Apply rolling window?', False)

    account = account_choice.selectbox('Select your savings account:',
                      options=accounts['name'].unique().tolist(),
                      placeholder='Choose your savings account')
    
    month_window = month_choice.number_input('Select how many months of funds:',
                                             min_value=1,
                                             step=1)
    
    month_data = None

    # Rolling Data Routine
    if is_rolling_window and rolling_data[1] < 6:
        month_data = rolling_data
        info_container.info(f'Less than 6 months of rolling data. Using available {rolling_data[1]} month(s) starting {rolling_data[0]}')
        expense_window = expenses.loc[\
            (expenses['value_date'].dt.date >= rolling_data[0]) &\
            (expenses['value_date'].dt.date <= today.date()) &\
            (expenses['nominal'] < 0)
        ]
    # Full Month Data Routine
    if not is_rolling_window and full_month_data[1] < 6:
        month_data = full_month_data
        info_container.info(f'Less than 6 months of full month data. Using available {full_month_data[1]} month(s) starting {full_month_data[0]}')
        expense_window = expenses.loc[\
            (expenses['value_date'].dt.date >= full_month_data[0]) &\
            (expenses['value_date'].dt.date < today.replace(day=1).date()) &\
            (expenses['nominal'] < 0)
        ]
    
if not average_expense:
    average_expense = expense_window['nominal'].sum()/month_data[1] * month_window

savings_account = accounts.loc[accounts['name'] == account].iloc[0]
st.dataframe(expense_window)
st.write(f'Expected Emergency Fund Size: {(average_expense) * (-1):.2f}')
st.write(f'Current Emergency Fund Size: {savings_account.nominal}')

yield_value = st.number_input('Enter yield in decimal:',
                                min_value=0.00,
                                value=savings_account['yield']
                            )

month_outlook = st.number_input('Enter number of months forward:',
                                min_value=1,
                                value=12,
                                step=1
                            )

def getFutureCashFlows(t_plus: int, start: float, apr: float):
    today = dt.date.today() 
    month_end = today + pd.offsets.MonthEnd()
    cfs = pd.DataFrame(columns=['date', 'nominal', 'cumulative_cf', 'cf'])
    for delta in range(t_plus+1):
        date = (today + pd.offsets.MonthEnd()) + relativedelta(months=delta)
        cf = apr/12 * start
        cumulative_cf = delta * cf
        new_nominal = start + cumulative_cf
        cfs.loc[len(cfs)] = [date, new_nominal, cumulative_cf, cf]
    
    return cfs

cf_data = getFutureCashFlows(month_outlook, savings_account.nominal, yield_value)
#cf_data = cf_data.set_index('date')
st.dataframe(cf_data)

difference = cf_data['nominal'] - [average_expense * -1 for _ in range(len(cf_data))]
expense_coverage_fig = go.Figure(
    data=[
        go.Scatter(x=cf_data['date'], y=cf_data['nominal'],
                mode='lines', line=go.scatter.Line(color='#18f3a8'),
                name='Expected Savings',
                hovertext=[f'Difference: {diff}' for diff in difference]),
        go.Scatter(x=cf_data['date'], y=[average_expense * -1 for _ in range(len(cf_data))],
                mode='lines', line=go.scatter.Line(color='crimson'),
                name='Savings Required',
                fill='tozeroy')
    ],
    layout=go.Layout(height=600, width=800, yaxis={'rangemode':'tozero'},
                     title='Expected Savings vs Expenses',
                     hovermode='x unified')
)

# net_cf = px.line(cf_data['nominal'], line_shape='spline',
#                  labels={
#                      "date": 'Date',
#                      'value': 'Nominal'
#                  },
#                  title='Net Cash Flow',
#                  range_y=[0, max(max(cf_data['nominal']) * 1.1 , average_expense * 1.1)])

# #net_cf.add_trace()
# net_cf.add_hline(y=average_expense * -1, line_width=2, line_color='red')
# net_cf.update_traces(line_color='#18f3a8')




expense_levels = pd.DataFrame(columns=['start_date', 'end_date', 'expense', 'expense_override', "expense_level"])
display_overrides = st.dataframe(expense_levels)
form = st.form('override', border=True)
start_date = form.date_input('Enter start date', value='today', key="override_form_start")
end_date = form.date_input('Enter start date', value='today', key="override_form_end")
expense_override = form.checkbox('Set actual expense level?')
expense = form.number_input('Enter expense', min_value=0, step=1)
submitted = form.form_submit_button("Submit")

if submitted:
    if expense_override:
        expense_levels.loc[len(expense_levels.index)] = [start_date, end_date, None, expense_override, expense]
        
    else:
        expense_levels.loc[len(expense_levels.index)] = [start_date, end_date, expense, expense_override, None]
    expense_levels.index = expense_levels.index + 1
    expense_levels = expense_levels.sort_index()
    display_overrides = st.dataframe(expense_levels)


st.plotly_chart(expense_coverage_fig, use_container_width=True)


    
# TODO: Handle no savings account

# TODO Prompt the user to input expected expenses at certain times
# and show the yield on the savings account or have them enter it and show if there is a need to cover,
# when and how much.

# TODO If account is below emergency threshold -> get yield and frequency of interest and show how long until 
# emergency funds are covered.


# st.write(DateManager.lastRollingMonthDate(test_dates))
# st.write(DateManager.lastEntireMonthDate(test_dates))