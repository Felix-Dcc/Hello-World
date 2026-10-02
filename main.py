from projects.rps import CHOICES, computer_choice, outcome
from terminal import ask, run, whole_number

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

ART = {'rock': rock, 'paper': paper, 'scissors': scissors}
RESULT = {'win': 'You win!', 'lose': 'Computer wins!', 'draw': "It's a draw!"}


def main():
    number = ask('What do you choose? Type 0 for rock, 1 for paper, 2 for scissors.\n',
                 whole_number(0, 2), 'Please type 0, 1 or 2.')
    player = CHOICES[number]
    print(ART[player])

    computer = computer_choice()
    print('Computer chose:\n', ART[computer])

    print(RESULT[outcome(player, computer)])


if __name__ == '__main__':
    run(main)
