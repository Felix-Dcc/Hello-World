import random
from hangman_art import logo, stages
from hangman_words import word_list

chosen_word = random.choice(word_list)

lives = 6

print(logo)
#Testing code
print(f'Pssst, the solution is {chosen_word}.')

display = []
for letter in chosen_word:
    display.append("_")
print(display)

end_of_game = False
while not end_of_game:
  guess = input("Guess a letter: ").lower()

  if guess in display:
     print(f"You've already guessed this letter, {guess}.")

  for i in range(len(chosen_word)):
    if chosen_word[i] == guess:
        display[i] = guess

  print(display) 

  if guess not in chosen_word:
   print(f"{guess} is not in the word. You lose a life")
   lives -= 1
   if lives == 0:
      end_of_game = True
      print("You lose")

   print(f"{' '.join(display)}")


  if "_" not in display:
     end_of_game = True
     print("You win")

  print(stages[lives])

