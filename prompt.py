from projects.atm import MAX_PIN_ATTEMPTS, Account, TransactionError, check_pin, money
from terminal import ask, run, whole_number


def main():
    for attempt in range(1, MAX_PIN_ATTEMPTS + 1):
        if check_pin(input('Please enter your pin ')):
            break
        left = MAX_PIN_ATTEMPTS - attempt
        print(f'You have entered a wrong pin. {left} attempt(s) left.' if left
              else 'Too many wrong attempts. Your card has been retained.')
    else:
        return

    account = Account()
    print("You're welcome!")
    while True:
        print('Click 1 to check your account balance')
        print('Click 2 to deposit money to your account')
        print('Click 3 to withdraw money')
        print('Click 4 to exit')
        option = ask('Please choose option ', whole_number(1, 4), 'Please type 1, 2, 3 or 4.')

        try:
            if option == 1:
                print(f'Your account balance is {money(account.balance)}')
            elif option == 2:
                amount = account.deposit(input('How much do you want to deposit? '))
                print(f'You have successfully deposited {money(amount)}')
                print(f'Your new balance is {money(account.balance)}')
            elif option == 3:
                amount = account.withdraw(input('Please enter amount you want to withdraw: '))
                print(f'You have successfully withdrawn {money(amount)}')
                print(f'Your new balance is {money(account.balance)}')
            else:
                print('Thank you. Goodbye!')
                return
        except TransactionError as e:
            print(f'Sorry: {e}')


if __name__ == '__main__':
    run(main)
