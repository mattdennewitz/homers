import datetime


def make_date(date):
    if isinstance(date, datetime.date):
        return date

    return datetime.date(
        *datetime.datetime.strptime(date, '%Y-%m-%d').timetuple()[:3])


def generate_year_series(year):
    current_date = datetime.date.today()
    yield current_date

    for step in range(0, (current_date.timetuple().tm_yday - 1)):
        current_date -= datetime.timedelta(days=1)
        yield current_date
