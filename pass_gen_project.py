from projects.password import MAX_PER_KIND, entropy_bits, generate, strength
from terminal import ask, run, whole_number


def main():
    print('Welcome to the Password Generator!')
    count = whole_number(0, MAX_PER_KIND)
    error = f'Please type a whole number from 0 to {MAX_PER_KIND}.'
    while True:
        letters = ask('How many letters would you like in your password?\n', count, error)
        symbols = ask('How many symbols would you like?\n', count, error)
        numbers = ask('How many numbers would you like?\n', count, error)
        try:
            password = generate(letters, symbols, numbers)
            break
        except ValueError as e:
            print(e)

    print(f'Your password is: {password}')
    print(f'Strength: {strength(entropy_bits(letters, symbols, numbers))}')


if __name__ == '__main__':
    run(main)
