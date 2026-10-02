"""The love calculator — just for fun."""


def love_score(name1, name2):
    """Count the letters of TRUE, then of LOVE, across both names and put the
    two counts side by side (E counts in both words)."""
    names = (name1 + name2).lower()
    true = sum(names.count(c) for c in 'true')
    love = sum(names.count(c) for c in 'love')
    return int(f'{true}{love}')


def verdict(score):
    if score < 10 or score > 90:
        return 'you go together like coke and bread'
    if 40 <= score <= 50:
        return 'you look alright together'
    return ''
