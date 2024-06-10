import random

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

user_choice = int(input("What do you choose? Type 0 for rock, 1 for paper, 2 for scissors.\n"))

if user_choice == 0:
    print(rock)
elif user_choice == 1:
    print(paper)
else:
    print(scissors)

computer_choice = random.choice(["0", "1", "2"])

if computer_choice == "0":
    print("Computer chose:\n", rock)
elif computer_choice == "1":
    print("Computer chose:\n", paper)
else:
    print("Computer chose:\n", scissors)

if user_choice == computer_choice:
    print("It's a draw!")
elif user_choice == "0" and computer_choice == "1":
    print("Computer wins!")
elif user_choice == "1" and computer_choice == "2":
    print("Computer wins!")
elif user_choice == "2" and computer_choice == "0":
    print("Computer wins!")
else:
    print("You win!")
