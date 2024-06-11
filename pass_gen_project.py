import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the Password Generator!")
num_of_letters = int(input("How many letters would you like in your password?\n")) 
num_of_symbols = int(input(f"How many symbols would you like?\n"))
num_of_numbers = int(input(f"How many numbers would you like?\n"))

password_list = []

for char in range(num_of_letters):
    password_list.append(random.choice(letters))
    letters.remove(password_list[-1])  

for char in range(num_of_symbols):
    password_list.append(random.choice(symbols))
    symbols.remove(password_list[-1]) 

for char in range(num_of_numbers):
    password_list.append(random.choice(numbers))
    numbers.remove(password_list[-1]) 

random.shuffle(password_list)
password = "".join(password_list)

print(f"Your password is: {password}")
