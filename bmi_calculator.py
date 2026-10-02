from projects.bmi import bmi, category, parse_height, parse_weight
from terminal import ask, run


def main():
    height = ask('What is your height in metres (e.g. 1.76)? ', parse_height,
                 'Please type a height between 0.5 and 2.75 metres, e.g. 1.76.')
    weight = ask('What is your weight in kg (e.g. 65)? ', parse_weight,
                 'Please type a weight between 2 and 650 kg, e.g. 65.')

    value = bmi(height, weight)
    print(f'Your BMI is {value:.1f}, {category(value)[1]}.')


if __name__ == '__main__':
    run(main)
