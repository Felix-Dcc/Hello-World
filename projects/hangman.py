"""Hangman: one game's state and rules."""
import random

from hangman_art import stages
from hangman_words import word_list

# stages[6] is the empty gallows and stages[0] the full figure, so the
# picture for the current state is simply stages[lives].
MAX_LIVES = len(stages) - 1


class Hangman:
    """A wrong letter costs one life the first time only; repeats and
    anything that isn't a single letter are rejected for free."""

    def __init__(self, word, lives=MAX_LIVES, guessed=()):
        self.word = word.lower()
        self.lives = lives
        self.guessed = list(guessed)

    @classmethod
    def new(cls, rng=random):
        return cls(rng.choice(word_list))

    def guess(self, text):
        """Play a letter. Returns 'hit', 'miss', 'repeat', 'invalid' or 'over'."""
        if self.over:
            return 'over'
        letter = text.strip().lower()
        if len(letter) != 1 or not (letter.isascii() and letter.isalpha()):
            return 'invalid'
        if letter in self.guessed:
            return 'repeat'
        self.guessed.append(letter)
        if letter in self.word:
            return 'hit'
        self.lives -= 1
        return 'miss'

    @property
    def masked(self):
        return [c if c in self.guessed else '_' for c in self.word]

    @property
    def misses(self):
        return [c for c in self.guessed if c not in self.word]

    @property
    def won(self):
        return all(c in self.guessed for c in self.word)

    @property
    def lost(self):
        return self.lives <= 0

    @property
    def over(self):
        return self.won or self.lost

    @property
    def picture(self):
        return stages[max(self.lives, 0)]

    def to_dict(self):
        return {'word': self.word, 'lives': self.lives, 'guessed': self.guessed}

    @classmethod
    def from_dict(cls, data):
        return cls(data['word'], data['lives'], data['guessed'])
