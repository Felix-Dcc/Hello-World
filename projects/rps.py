"""Rock, paper, scissors."""
import random

CHOICES = ('rock', 'paper', 'scissors')
BEATS = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}


def outcome(player, computer):
    """'win', 'lose' or 'draw', from the player's side."""
    if player not in BEATS or computer not in BEATS:
        raise ValueError('Choose rock, paper or scissors')
    if player == computer:
        return 'draw'
    return 'win' if BEATS[player] == computer else 'lose'


def computer_choice(rng=random):
    return rng.choice(CHOICES)
