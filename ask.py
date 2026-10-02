from projects.rollercoaster import MIN_HEIGHT_CM, quote
from terminal import ask, run, whole_number, yes_no


def main():
    print('WELCOME TO THE ROLLERCOASTER!')
    height = ask('What is your height in cm? ', whole_number(50, 250),
                 'Please type your height in cm, between 50 and 250.')
    if height < MIN_HEIGHT_CM:
        print('Sorry, you can not ride the rollercoaster! You need a height of '
              f'at least {MIN_HEIGHT_CM}cm to ride the rollercoaster.')
        return

    print('You can ride the rollercoaster!')
    age = ask('What is your age? ', whole_number(1, 120), 'Please type an age between 1 and 120.')
    photo = ask('Do you want photos? Y or N \n', yes_no)

    bill = quote(height, age, photo)
    print(f'Ticket is {bill.ticket}ghc' if bill.ticket else 'Ticket is free. Enjoy ur ride!')
    print(f'Your final bill is Ghc{bill.total}')


if __name__ == '__main__':
    run(main)
