import datetime


def make_date(date):
    if isinstance(date, datetime.date):
        return date

    return datetime.date(
        *datetime.datetime.strptime(date, '%Y-%m-%d').timetuple()[:3])


def generate_year_series(year):
    """Generate a series of dates within, roughly, the entire season.
    """

    today = datetime.date.today()

    if year == today.year:
        current_date = today
    else:
        # arbitrary end date
        current_date = datetime.date(year, 11, 15)

    min_date = datetime.date(year, 3, 1)

    while current_date >= min_date:
        yield current_date
        current_date -= datetime.timedelta(days=1)
