"""Unit tests for the shared logic in projects/."""
import random
import string
import time
from decimal import Decimal
from pathlib import Path

import pytest

from projects import (atm, bmi, chemistry, hangman, leap_year, love, password, pizza,
                      rollercoaster, rps, treasure_island, tree)

ROOT = Path(__file__).resolve().parent.parent


# -- Hangman -------------------------------------------------------------------

def test_hangman_wrong_letter_costs_one_life_only_once():
    game = hangman.Hangman('cycle')
    assert game.guess('q') == 'miss'
    assert game.guess('q') == 'repeat'
    assert game.guess('Q') == 'repeat'
    assert game.lives == hangman.MAX_LIVES - 1


@pytest.mark.parametrize('bad', ['', ' ', 'ab', '1', '!', 'é'])
def test_hangman_rejects_anything_but_one_letter_for_free(bad):
    game = hangman.Hangman('cycle')
    assert game.guess(bad) == 'invalid'
    assert game.lives == hangman.MAX_LIVES
    assert game.guessed == []


def test_hangman_win_reveals_every_copy_of_a_letter():
    game = hangman.Hangman('cycle')
    for letter in 'cyle':
        assert game.guess(letter) == 'hit'
    assert game.masked == list('cycle')
    assert game.won and game.over and not game.lost


def test_hangman_loses_after_max_lives_and_then_ignores_guesses():
    game = hangman.Hangman('cycle')
    for letter in 'abdfgh':
        game.guess(letter)
    assert game.lost and game.lives == 0
    assert game.guess('c') == 'over'
    assert game.picture == hangman.stages[0]


def test_hangman_round_trips_through_a_dict():
    game = hangman.Hangman('cycle')
    game.guess('c')
    game.guess('z')
    copy = hangman.Hangman.from_dict(game.to_dict())
    assert (copy.word, copy.lives, copy.guessed, copy.misses) == ('cycle', 5, ['c', 'z'], ['z'])


def test_hangman_words_are_all_plain_lowercase_letters():
    assert all(w.isascii() and w.isalpha() and w.islower() for w in hangman.word_list)


# -- Rock, paper, scissors -----------------------------------------------------

@pytest.mark.parametrize('player, computer, result', [
    ('rock', 'scissors', 'win'), ('rock', 'paper', 'lose'), ('rock', 'rock', 'draw'),
    ('paper', 'rock', 'win'), ('paper', 'scissors', 'lose'), ('paper', 'paper', 'draw'),
    ('scissors', 'paper', 'win'), ('scissors', 'rock', 'lose'), ('scissors', 'scissors', 'draw'),
])
def test_rps_every_pairing(player, computer, result):
    assert rps.outcome(player, computer) == result


def test_rps_player_does_not_always_win():
    # The old script compared an int to a str, so every game was "You win!".
    results = {rps.outcome('rock', rps.computer_choice(random.Random(seed))) for seed in range(60)}
    assert results == {'win', 'lose', 'draw'}


def test_rps_rejects_unknown_choice():
    with pytest.raises(ValueError):
        rps.outcome('lizard', 'rock')


# -- Password generator --------------------------------------------------------

@pytest.mark.parametrize('letters, symbols, numbers', [(8, 10, 2), (8, 2, 11), (0, 50, 50), (1, 0, 0)])
def test_password_has_exactly_the_requested_mix(letters, symbols, numbers):
    pw = password.generate(letters, symbols, numbers)
    assert len(pw) == letters + symbols + numbers
    assert sum(c in string.ascii_letters for c in pw) == letters
    assert sum(c in password.SYMBOLS for c in pw) == symbols
    assert sum(c in string.digits for c in pw) == numbers


def test_password_uses_a_secure_random_source():
    assert isinstance(password._rng, random.SystemRandom)


@pytest.mark.parametrize('args', [(0, 0, 0), (-1, 2, 2), (51, 0, 0), (2.5, 1, 1), (True, 1, 1)])
def test_password_rejects_bad_counts(args):
    with pytest.raises(ValueError):
        password.generate(*args)


def test_password_entropy_and_strength():
    # one letter: 52 choices, nothing to arrange
    assert password.entropy_bits(1, 0, 0) == pytest.approx(5.70, abs=0.01)
    # one letter + one number: 52 * 10 choices, 2 orders
    assert password.entropy_bits(1, 0, 1) == pytest.approx(10.02, abs=0.01)
    assert password.strength(password.entropy_bits(4, 0, 0)) == 'Very weak'
    assert password.strength(password.entropy_bits(10, 2, 2)) == 'Strong'
    assert password.strength(password.entropy_bits(20, 4, 4)) == 'Very strong'


# -- ATM -----------------------------------------------------------------------

def test_atm_pin_check():
    assert atm.check_pin('2050') and atm.check_pin(' 2050 ')
    assert not atm.check_pin('2051') and not atm.check_pin('')


def test_atm_deposit_and_withdraw_track_balance_and_history():
    account = atm.Account()
    account.deposit('250.50')
    account.withdraw('1,000')
    assert account.balance == Decimal('250.50')
    assert account.history == [('Deposit', '250.50', '1250.50'), ('Withdrawal', '1000.00', '250.50')]


@pytest.mark.parametrize('amount', ['-500', '0', '-0', 'abc', '', 'NaN', 'Infinity', '12.345', '1e7'])
def test_atm_refuses_bad_amounts_without_touching_the_balance(amount):
    # A negative withdrawal used to add money; a negative deposit took it away.
    account = atm.Account()
    for move in (account.deposit, account.withdraw):
        with pytest.raises(atm.TransactionError):
            move(amount)
    assert account.balance == atm.OPENING_BALANCE and account.history == []


def test_atm_refuses_overdraft():
    account = atm.Account()
    with pytest.raises(atm.TransactionError, match='Insufficient funds'):
        account.withdraw('1000.01')
    account.withdraw('1000')
    assert account.balance == 0


def test_atm_round_trips_through_a_dict_without_float_drift():
    account = atm.Account()
    for _ in range(10):
        account.deposit('0.10')
    copy = atm.Account.from_dict(account.to_dict())
    assert copy.balance == Decimal('1001.00')
    assert len(copy.history) == 10


# -- Rollercoaster -------------------------------------------------------------

@pytest.mark.parametrize('age, price', [
    (15, 20), (20, 20), (25, 20), (26, 30), (30, 30), (31, 40), (40, 40), (44, 40),
    (45, 0), (55, 0), (56, 40), (90, 40),
])
def test_rollercoaster_every_age_has_a_price(age, price):
    # Ages under 20, 36-44 and over 55 used to ride for GHS 0 with no message.
    assert rollercoaster.quote(150, age).ticket == price


def test_rollercoaster_height_rule_and_photo():
    assert rollercoaster.quote(119, None).can_ride is False
    q = rollercoaster.quote(120, 28, photo=True)
    assert (q.can_ride, q.ticket, q.photo, q.total) == (True, 30, 3, 33)


@pytest.mark.parametrize('height, age', [(40, 20), (300, 20), (150, None), (150, 0), (150, 130)])
def test_rollercoaster_rejects_impossible_input(height, age):
    with pytest.raises(ValueError):
        rollercoaster.quote(height, age)


# -- BMI -----------------------------------------------------------------------

def test_bmi_value_and_categories():
    assert bmi.bmi(1.75, 70) == pytest.approx(22.86, abs=0.01)
    assert [bmi.category(v)[0] for v in (18.4, 18.5, 24.9, 25, 29.9, 30, 34.9, 35)] == [
        'under', 'normal', 'normal', 'over', 'over', 'obese', 'obese', 'severe']


def test_bmi_accepts_decimal_weight_and_height_in_cm():
    # int() used to crash on 70.5; 175 used to be read as 175 metres.
    assert bmi.parse_weight('70.5') == 70.5
    assert bmi.parse_height('175') == pytest.approx(1.75)
    assert bmi.parse_height('1.75') == 1.75


@pytest.mark.parametrize('height', ['0', '0.3', '2.8', '400'])
def test_bmi_rejects_impossible_heights(height):
    with pytest.raises(ValueError):
        bmi.parse_height(height)


# -- Leap year -----------------------------------------------------------------

@pytest.mark.parametrize('year, leap', [(2024, True), (2023, False), (1900, False), (2000, True), (4, True)])
def test_leap_years(year, leap):
    assert leap_year.is_leap(year) is leap


def test_leap_year_reason_and_next():
    assert 'not by 400' in leap_year.reason(1900)
    assert leap_year.next_leap(2024) == 2028
    assert leap_year.next_leap(2096) == 2104      # 2100 is skipped


@pytest.mark.parametrize('year', [0, -4, 10000, '2024', 2024.0])
def test_leap_year_rejects_out_of_range(year):
    with pytest.raises(ValueError):
        leap_year.is_leap(year)


# -- Love calculator -----------------------------------------------------------

def test_love_score_matches_the_original_formula():
    # "angela yu" + "jack bauer": T R U E -> 0+1+2+2 = 5; L O V E -> 1+0+0+2 = 3
    assert love.love_score('Angela Yu', 'Jack Bauer') == 53
    assert love.love_score('', '') == 0
    assert love.verdict(5) and love.verdict(45) and love.verdict(64) == ''


# -- Pizza ---------------------------------------------------------------------

def test_pizza_quote_is_case_insensitive():
    # A lowercase 'm' used to cost $0 for the pizza and $3 for the pepperoni.
    items, total = pizza.quote('m', pepperoni=True)
    assert items == [('Medium pizza', 20), ('Pepperoni', 3)] and total == 23
    assert pizza.quote('Large', cheese=True)[1] == 26
    assert pizza.quote('S', True, True)[1] == 18


def test_pizza_rejects_unknown_size():
    with pytest.raises(ValueError):
        pizza.quote('XL', pepperoni=True)


# -- Treasure Island -----------------------------------------------------------

def test_treasure_island_winning_path():
    scene = treasure_island.START
    for answer in ('Left', 'wait', 'YELLOW'):
        scene = treasure_island.step(scene, answer)
    ending = treasure_island.STORY[scene]
    assert isinstance(ending, treasure_island.Ending) and ending.won


def test_treasure_island_unknown_answer_keeps_you_in_the_same_scene():
    with pytest.raises(ValueError, match='Red, Blue, Yellow'):
        treasure_island.step('doors', 'green')


def test_treasure_island_every_choice_leads_somewhere_real():
    for scene in treasure_island.STORY.values():
        if isinstance(scene, treasure_island.Scene):
            assert all(target in treasure_island.STORY for target in scene.choices.values())


# -- Chemical formula lookup ---------------------------------------------------

@pytest.mark.parametrize('bad', ['', 'hello', 'c6h6', '6CH', 'C' * 41, 'H2O;'])
def test_chemistry_rejects_malformed_formulas_before_any_request(bad):
    called = []
    with pytest.raises(chemistry.InvalidFormula):
        chemistry.lookup(bad, search=called.append)
    assert called == []


def test_chemistry_passes_a_cleaned_formula_to_the_search():
    found = chemistry.Compound('C6H6', 241, 'benzene', 'Benzene', '78.11')
    seen = []
    result = chemistry.lookup(' C6 H6 ', search=lambda f: seen.append(f) or found)
    assert seen == ['C6H6'] and result.url.endswith('/compound/241')


def test_chemistry_times_out_instead_of_hanging():
    with pytest.raises(chemistry.Unavailable, match='too long'):
        chemistry.lookup('H2O', search=lambda f: time.sleep(1), timeout=0.05)


def test_chemistry_handles_missing_synonyms_and_network_errors(monkeypatch):
    pcp = pytest.importorskip('pubchempy')

    class Bare:
        cid, iupac_name, molecular_weight, synonyms = 962, 'oxidane', 18.015, []

    monkeypatch.setattr(pcp, 'get_compounds', lambda *a: [Bare()])
    c = chemistry.lookup('H2O')
    assert (c.name, c.common_name, c.weight) == ('oxidane', None, '18.015')

    monkeypatch.setattr(pcp, 'get_compounds', lambda *a: [])
    with pytest.raises(chemistry.NotFound):
        chemistry.lookup('H2O')

    def offline(*a):
        raise OSError('network is unreachable')
    monkeypatch.setattr(pcp, 'get_compounds', offline)
    with pytest.raises(chemistry.Unavailable):
        chemistry.lookup('H2O')


# -- Christmas tree ------------------------------------------------------------

ORIGINAL_TREE = '\n'.join([
    *(' ' * (15 - i) + '*' * (2 * i + 1) for i in range(9)),
    '               || ', '               || ', '               || ',
    '             \\=======/',
])


def test_tree_default_matches_the_original_output():
    assert tree.christmas_tree() == ORIGINAL_TREE


def test_tree_scales():
    small = tree.christmas_tree(3, margin=0).splitlines()
    assert small[:3] == ['  *', ' ***', '*****']
    with pytest.raises(ValueError):
        tree.christmas_tree(0)
