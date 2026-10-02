"""Password generator."""
import math
import secrets
import string

LETTERS = string.ascii_letters
NUMBERS = string.digits
SYMBOLS = '!#$%&()*+'
MAX_PER_KIND = 50

# A password must not be predictable, so draw from the OS's secure random
# source rather than the random module.
_rng = secrets.SystemRandom()


def _check(letters, symbols, numbers):
    for name, n in (('letters', letters), ('symbols', symbols), ('numbers', numbers)):
        if isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= MAX_PER_KIND:
            raise ValueError(f'Number of {name} must be a whole number from 0 to {MAX_PER_KIND}')
    if letters + symbols + numbers == 0:
        raise ValueError('Ask for at least one character')


def generate(letters, symbols, numbers, rng=_rng):
    """Characters are drawn with replacement, so any count works (the old
    version removed each pick and crashed past 9 symbols or 10 numbers)."""
    _check(letters, symbols, numbers)
    chars = ([rng.choice(LETTERS) for _ in range(letters)]
             + [rng.choice(SYMBOLS) for _ in range(symbols)]
             + [rng.choice(NUMBERS) for _ in range(numbers)])
    rng.shuffle(chars)
    return ''.join(chars)


def entropy_bits(letters, symbols, numbers):
    """Exact entropy of generate(): each character's pool, plus the ways the
    three kinds can be arranged (the pools don't overlap)."""
    _check(letters, symbols, numbers)
    total = letters + symbols + numbers
    arrangements = math.comb(total, letters) * math.comb(total - letters, symbols)
    return (letters * math.log2(len(LETTERS))
            + symbols * math.log2(len(SYMBOLS))
            + numbers * math.log2(len(NUMBERS))
            + math.log2(arrangements))


def strength(bits):
    """A label for a password's entropy in bits."""
    for limit, label in ((28, 'Very weak'), (36, 'Weak'), (60, 'Fair'), (128, 'Strong')):
        if bits < limit:
            return label
    return 'Very strong'
