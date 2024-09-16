from datetime import datetime, timedelta


def extract_month_and_year(filename):
    """
    Extracts the month and year from the given cvs file.
    The filename has this format 'spata_venizelos_{int(year)}_{int(month)}.csv'
    """
    try:
        month = int(filename[21:-4])
        year = int(filename[16:20])
        return month, year
    except ValueError:
        print("Wrong File Name Format.")
    except TypeError:
        print("Wrong File Name Format.")


def generate_dates(month, year):
    """Generates a list of dates within the specified month and year."""
    day = timedelta(days=1)
    d = datetime(year, month, 1)
    dates = []
    while d.month == month:
        dates.append(d.strftime('%Y-%m-%d'))
        d += day
    return dates


class DateGenerator:
    """Generates a list of dates within a given month."""

    def __init__(self, filename):
        self.filename = filename

    def get_dates(self):
        """Returns a list of dates."""
        month, year = extract_month_and_year(self.filename)
        return generate_dates(month, year)

    def get_month_year(self):
        """Returns the month and year extracted from the filename."""
        return extract_month_and_year(self.filename)
