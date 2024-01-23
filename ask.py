print("WELCOME TO THE ROLLERCOASTER!")

height = int(input("What is your height in cm?"))
height >= 120
bill = 0

if height >= 120:
    print("You can ride the rollercoaster!")
    age = int(input("What is your age?"))
    if 20 <= age <= 25:
        bill = 20
        print("Ticket is 20ghc")
    elif 26 <= age <= 30:
        bill = 30
        print("Ticket is 30ghc")
    elif 31 <= age <= 35:
        bill = 40
        print("Ticket is 40ghc")
    
    want_photo = input("Do you want photos? Y or N \n")
    if want_photo == "Y":
        bill += 3

    print(f"Your final bill is Ghc{bill}")

else:
    print("Sorry, you can not ride the rollercoaster! You need a height of atleast 120cm to ride the rollercoaster.")
    