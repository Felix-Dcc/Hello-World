#Just for fun!
from projects.love import love_score, verdict
from terminal import run


def main():
    print('The love calculator is calculating your score... ')
    name1 = input('What is your name? ')
    name2 = input('What is their name? ')

    score = love_score(name1, name2)
    message = verdict(score)
    print(f'Your score is {score}, {message}.' if message else f'Your score is {score}.')


if __name__ == '__main__':
    run(main)
