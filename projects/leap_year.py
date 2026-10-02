"""Gregorian leap years."""


def check_year(year):
    if isinstance(year, bool) or not isinstance(year, int) or not 1 <= year <= 9999:
        raise ValueError('Enter a year from 1 to 9999')
    return year


def is_leap(year):
    check_year(year)
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def reason(year):
    """Which part of the rule decided it."""
    if year % 4:
        return f'{year} is not divisible by 4.'
    if year % 100:
        return f'{year} is divisible by 4 and not by 100.'
    if year % 400:
        return f'{year} is divisible by 100 but not by 400.'
    return f'{year} is divisible by 400.'


def next_leap(year):
    """The first leap year after this one."""
    year += 1
    while not is_leap(year):
        year += 1
    return year
