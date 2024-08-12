import pandas as pd
from wp.managers.watchpoint_manager import WatchPointManager

class NetWorthAnalyzer:
    @staticmethod
    def getNetworthMetrics():
        df = WatchPointManager.loadNetWorthDF()
        # Aggregate to get the last reading of each day
        # Assume today is '2024-01-01'
        today = pd.Timestamp.today()

                # Get the last record for today
        today_df = df[df['date'].dt.date == today.date()].tail(1)
        data = {
            "DoD":[None, None],
            "MoM":[None, None],
            "YoY":[None, None],
            "TtD":[None, None]
        }

        if not today_df.empty:
            today_net_worth = today_df.iloc[0]['net_worth']
            
            # Get the last record of the previous day
            previous_day = today - pd.Timedelta(days=1)
            previous_day_df = df[df['date'].dt.date == previous_day.date()].tail(1)
            if not previous_day_df.empty:
                previous_day_net_worth = previous_day_df.iloc[0]['net_worth']
                data['DoD'] = [today_net_worth - previous_day_net_worth,
                    ((today_net_worth - previous_day_net_worth) / previous_day_net_worth) * 100]
            else:
                # Fallback to first record if no previous day data is available
                first_record_net_worth = df.iloc[0]['net_worth']
                data['DoD'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]
            
            # Get the last record of the previous month
            previous_month = today - pd.DateOffset(months=1)
            previous_month_df = df[(df['date'].dt.year == previous_month.year) & (df['date'].dt.month == previous_month.month)].tail(1)
            if not previous_month_df.empty:
                previous_month_net_worth = previous_month_df.iloc[0]['net_worth']
                data['MoM'] = [today_net_worth - previous_month_net_worth,
                    ((today_net_worth - previous_month_net_worth) / previous_month_net_worth) * 100]
            else:
                # Fallback to first record if no previous month data is available
                first_record_net_worth = df.iloc[0]['net_worth']
                data['MoM'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]
            
            # Get the last record of the previous year
            previous_year = today - pd.DateOffset(years=1)
            previous_year_df = df[(df['date'].dt.year == previous_year.year) & (df['date'].dt.month == today.month) & (df['date'].dt.day == today.day)].tail(1)
            if not previous_year_df.empty:
                previous_year_net_worth = previous_year_df.iloc[0]['net_worth']
                data['YoY'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - previous_year_net_worth) / previous_year_net_worth) * 100]
            else:
                # Fallback to first record if no previous year data is available
                first_record_net_worth = df.iloc[0]['net_worth']
                data['YoY'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]
            
            # Calculate all-time growth
            first_record_net_worth = df.iloc[0]['net_worth']
            data['TtD'] = [today_net_worth - first_record_net_worth,
                    ((today_net_worth - first_record_net_worth) / first_record_net_worth) * 100]


        return data