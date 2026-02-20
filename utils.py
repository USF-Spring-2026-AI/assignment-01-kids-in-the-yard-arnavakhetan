import random


def year_to_decade_label(year):
    """Convert a year like 1950 to a label like 1950s."""
    decade_start = (year // 10) * 10
    return f"{decade_start}s"

def clamp_int(value, low, high):
    """Clamp an integer to [low, high]."""
    return max(low, min(high, value))

def ceil_to_int(x):
    """
    Return ceil(x) as an int.
    Assumes x is a float or int.
    """
    i = int(x)
    if x == i:
        return i
    return i + 1

def evenly_spaced_years(start_year, end_year, count):
    """Return 'count' evenly spaced integer years from start_year to end_year inclusive."""
    if count <= 0:
        return []
    if count == 1:
        return [start_year]

    step = (end_year - start_year) / (count - 1)
    years = []
    i = 0
    while i < count:
        year = int(round(start_year + i * step))
        years.append(year)
        i += 1

    years[0] = start_year
    years[-1] = end_year
    return years