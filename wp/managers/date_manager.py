import datetime as dt
from dateutil import relativedelta

class DateManager:
    @staticmethod
    def hasSixMonths(dates):
        today = dt.datetime.now()
        return {'rolling_months': min(dates) > (today - relativedelta(months=6)).date(),
                'entire_months':min(dates) > today.replace(day=1, month=((today.month - 6 - 1) % 12 + 1)).date()}

    @staticmethod
    def lastRollingMonthDate(dates):
        today = dt.datetime.now()
        month_diff = today.month - min(dates).month 
        day_diff = today.day - min(dates).day

        if month_diff == 0 or (month_diff == 1 and day_diff < 0):
            return [None, None, 'rolling']
        elif day_diff >= 0:
            return [(today - relativedelta(months=month_diff)).date(), month_diff, 'rolling']
        else:
            return [(today - relativedelta(months=month_diff-1)).date(), month_diff - 1, 'rolling']

    @staticmethod
    def lastEntireMonthDate(dates):
        today = dt.datetime.now()
        first_day = today.replace(day=1)
        if min(dates).day != 1:
            month_diff = first_day.month - (min(dates) + relativedelta(months=1)).month
        else:
            month_diff = first_day.month - min(dates).month

        if month_diff < 1:
            return [None, None, 'entire']
        else:
            return [(first_day - relativedelta(months=month_diff)).date(), month_diff, 'entire']
        