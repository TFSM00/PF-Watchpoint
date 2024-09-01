import streamlit as st
from wp.managers.watchpoint_manager import ExpensesManager as em, WatchPointManager as wm
import plotly.express as px
import datetime as dt
from wp.startup import startup

startup()

expense_df = em.loadExpenses()
today = dt.datetime.now()
data = {
    'Income': expense_df.loc[expense_df['nominal'] > 0],
    'Expenses': expense_df.loc[expense_df['nominal'] < 0]
}

st.header('Expense Analysis')
analysis_type_col, cash_flow_col = st.columns(2)

analysis_type = analysis_type_col.selectbox('Select analysis type:', options=['All-Time', 'Yearly', 'Monthly'])
cash_flow_type = cash_flow_col.selectbox('Select cash flow type:', options=['Income', 'Expenses'])

match analysis_type:
    case 'All-Time':
        pie_dataset = data[cash_flow_type]
        bar_dataset = expense_df

    case 'Yearly':
        graph_year = st.selectbox('Select year:', 
                          options=data[cash_flow_type]['value_date'].dt.year.unique().tolist())
        
        pie_dataset = data[cash_flow_type].loc[data[cash_flow_type]['value_date'].dt.year == graph_year]
        bar_dataset = expense_df.loc[expense_df['value_date'].dt.year == graph_year]

    case 'Monthly':
        graph_year_col, graph_month_col = st.columns(2)

        graph_year = graph_year_col.selectbox('Select year:', 
                          options=data[cash_flow_type]['value_date'].dt.year.unique().tolist())
        

        graph_month = graph_month_col.selectbox('Select month:', 
                                options=list(map(wm.getMonthName, data[cash_flow_type]['value_date'].dt.month.unique()))[::-1],
                                )

        pie_dataset = data[cash_flow_type].loc[(data[cash_flow_type]['value_date'].dt.year == graph_year) &\
                                (data[cash_flow_type]['value_date'].dt.month == wm.getMonthNumber(graph_month))]
        
        bar_dataset = expense_df.loc[(expense_df['value_date'].dt.year == graph_year) &\
                                     (expense_df['value_date'].dt.month == wm.getMonthNumber(graph_month))]

#st.dataframe(pie_dataset)
pie_chart = px.pie(names=pie_dataset['category'], values=pie_dataset['nominal'].abs(),
                   title="Cash Flow as Percentage of Date Total")
pie_chart.update_traces(textfont_size=14)

st.plotly_chart(pie_chart, use_container_width=True)

bar_chart = px.bar(bar_dataset, x='value_date', y='nominal', color='category',
                   labels = {
                       "value_date": "Date",
                       "nominal": "Nominal",
                       "category": "Category"
                   },
                   title="Cash Flow by Date and Category")

st.plotly_chart(bar_chart, use_container_width=True)



resample_mode = 'D' if analysis_type != 'All-Time' else 'ME'
net_cf_dataset = bar_dataset.resample(resample_mode, on='value_date')['nominal'].sum()
#colors = ['red' if val < 0 else 'green' for val in net_cf_dataset.values]
net_cf = px.line(net_cf_dataset, line_shape='spline',
                 labels={
                     "value_date": 'Date',
                     'value': 'Nominal',
                     'variable': 'Variable'
                 },
                 title='Net Cash Flow')


net_cf.add_hline(y=0, line_width=2, line_color='white')
net_cf.update_traces(line_color='#18f3a8')
st.plotly_chart(net_cf, use_container_width=True)
# st.dataframe(net_cf_dataset)
# st.write(net_cf_dataset.columns)