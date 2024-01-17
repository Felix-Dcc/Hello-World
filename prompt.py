account_balance = float(1000)
pin = int(2050)

account_pin = int(input("Please enter your pin "))
while True:
 if account_pin == pin:
    print("You're welcome!")
    print("Click 1 to check your account balance")
    print("Click 2 to deposit money to your account")
    print("Click 3 to withdraw money")
  
    option = int(input("Please choose option "))
    if option == 1:
        print(f"Your account balance is GHS {account_balance}")
    if option == 2:
          depo = int(input("How much do you want to deposit"))
          account_balance+=depo
          print(f"You have successfully deposited GHS {depo}")
          print(f"Your new balance is GHS {account_balance}")
    if option == 3:
        amount = int(input("Please enter amount you want to withdraw"))
        if amount > account_balance:
           print("Sorry, the money is insufficient!")
        else:
           print(f"You have successfully withdrawn GHS {amount}")
           total_amount=account_balance-amount
           account_balance=total_amount 
           print(f"Your new balance is GHS {account_balance}")
 else:
    print("You have entered a wrong pin, try again")
    break