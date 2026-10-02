from hangman_art import logo
from projects.hangman import Hangman
from terminal import run


def main():
    game = Hangman.new()
    print(logo)
    print(' '.join(game.masked))

    while not game.over:
        guess = input('Guess a letter: ').strip().lower()
        result = game.guess(guess)
        if result == 'invalid':
            print('Please type a single letter.')
            continue
        if result == 'repeat':
            print(f"You've already guessed {guess}.")
        elif result == 'miss':
            print(f'{guess} is not in the word. You lose a life.')
        print(' '.join(game.masked))
        print(game.picture)

    print('You win!' if game.won else f'You lose. The word was {game.word}.')


if __name__ == '__main__':
    run(main)
