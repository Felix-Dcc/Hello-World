from projects.pizza import parse_size, quote
from terminal import ask, run, yes_no


def main():
    print('Thank you for choosing Python Pizza Deliveries!')
    size = ask('What size pizza do you want? S, M, or L? ', parse_size)
    pepperoni = ask('Do you want pepperoni? Y or N? ', yes_no)
    cheese = ask('Do you want extra cheese? Y or N? ', yes_no)

    items, total = quote(size, pepperoni, cheese)
    for name, price in items:
        print(f'  {name:<14} ${price}')
    print(f'Your final bill is: ${total}.')


if __name__ == '__main__':
    run(main)
