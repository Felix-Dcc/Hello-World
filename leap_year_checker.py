from projects.leap_year import is_leap, reason
from terminal import ask, run, whole_number


def main():
    year = ask('Which year do you want to check? ', whole_number(1, 9999),
               'Please type a year from 1 to 9999.')
    print('It is a leap year.' if is_leap(year) else 'It is not a leap year.')
    print(reason(year))


if __name__ == '__main__':
    run(main)
