from datetime import datetime, timedelta


def get_date(days):
    f = (datetime.now() - timedelta(days=days)).date()
    return f
