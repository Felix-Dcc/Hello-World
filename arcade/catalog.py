"""The projects shown on the home page, grouped."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Project:
    slug: str          # template name and the view's endpoint
    title: str
    icon: str
    blurb: str
    script: str        # the terminal version at the repo root


CATEGORIES = [
    ('Games', [
        Project('hangman', 'Hangman', '🔤', 'Guess the word one letter at a time.', 'Hangman.py'),
        Project('rps', 'Rock, paper, scissors', '✊', 'Best of as many rounds as you like.', 'main.py'),
        Project('treasure_island', 'Treasure Island', '🏝️', 'Choose your path and find the treasure.',
                'treasure_island_project.py'),
    ]),
    ('Everyday tools', [
        Project('password', 'Password generator', '🔐', 'Strong random passwords, your mix.',
                'pass_gen_project.py'),
        Project('bmi', 'BMI calculator', '⚖️', 'Body mass index from height and weight.',
                'bmi_calculator.py'),
        Project('leap_year', 'Leap year checker', '📅', 'Is it a leap year, and why?',
                'leap_year_checker.py'),
        Project('chemistry', 'Chemical formula lookup', '🧪', 'Names and weight from PubChem.',
                'ChemicalFormula.py'),
    ]),
    ('Shop and bank', [
        Project('atm', 'ATM', '🏧', 'Check, deposit and withdraw on a demo account.', 'prompt.py'),
        Project('pizza', 'Python Pizza', '🍕', 'Build an order and see the bill.',
                'pizza_delivery_test.py'),
        Project('rollercoaster', 'Rollercoaster tickets', '🎢', 'Can you ride, and what does it cost?',
                'ask.py'),
    ]),
    ('Just for fun', [
        Project('love', 'Love calculator', '💘', 'The very scientific TRUE LOVE test.',
                'love_calculator.py'),
        Project('tree', 'Christmas tree', '🎄', 'Grow an ASCII tree to any height.', 'ChristmasTree.py'),
    ]),
]

PROJECTS = {p.slug: p for _, group in CATEGORIES for p in group}
