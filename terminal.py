"""Prompt helpers shared by the terminal scripts."""
import sys


def ask(prompt, parse=str, error=None):
    """Ask until parse(answer) succeeds; parse raises ValueError on bad input.
    Prints `error`, or else the ValueError's own message, before asking again."""
    while True:
        answer = input(prompt)
        try:
            return parse(answer)
        except ValueError as e:
            print(error or str(e) or 'Please try again.')


def whole_number(low, high):
    def parse(text):
        value = int(text)
        if not low <= value <= high:
            raise ValueError
        return value
    return parse


def yes_no(text):
    answer = text.strip().lower()
    if answer in ('y', 'yes'):
        return True
    if answer in ('n', 'no'):
        return False
    raise ValueError('Please answer Y or N.')


def run(main):
    """Run a script's main(), leaving quietly on Ctrl-C or Ctrl-D."""
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print('\nBye!')
        sys.exit(0)
