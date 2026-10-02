"""The terminal scripts, driven through stdin like a person would."""
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def run(script, stdin, seed=None):
    """Run a script from the repo root; optionally seed random first."""
    code = (f'import random, runpy; random.seed({seed}); '
            f'runpy.run_path({script!r}, run_name="__main__")')
    result = subprocess.run([sys.executable, '-c', code], input=stdin, cwd=ROOT,
                            capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_rps_can_lose_and_rejects_invalid_choices():
    outcomes = {run('main.py', '0\n', seed).strip().splitlines()[-1] for seed in range(12)}
    assert outcomes == {'You win!', 'Computer wins!', "It's a draw!"}
    out = run('main.py', '7\nrock\n1\n', 0)
    assert out.count('Please type 0, 1 or 2.') == 2


def test_hangman_hides_the_answer_and_charges_a_wrong_letter_once():
    out = run('Hangman.py', 'q\nq\n\nab\n' + 'zxjkvw'.replace('', '\n')[1:], seed=1)
    assert 'solution' not in out
    assert out.count('q is not in the word') == 1
    assert "You've already guessed q." in out
    assert out.count('Please type a single letter.') == 2


def test_password_generator_handles_large_counts():
    out = run('pass_gen_project.py', '8\n10\n11\n')
    password = out.split('Your password is: ')[1].split()[0]
    assert len(password) == 29
    assert 'Strength:' in out


def test_password_generator_reasks_on_nonsense():
    out = run('pass_gen_project.py', 'ten\n-1\n4\n0\n0\n')
    assert out.count('Please type a whole number') == 2
    assert len(out.split('Your password is: ')[1].split()[0]) == 4


def test_atm_refuses_negative_amounts_and_can_exit():
    out = run('prompt.py', '2050\n3\n-500\n2\n-5000\n1\n4\n')
    assert out.count('Sorry: Enter an amount greater than zero') == 2
    assert 'Your account balance is GHS 1,000.00' in out
    assert 'Goodbye' in out


def test_atm_allows_three_pin_attempts():
    out = run('prompt.py', '1111\n2222\n2050\n4\n')
    assert '2 attempt(s) left' in out and '1 attempt(s) left' in out
    assert "You're welcome!" in out
    out = run('prompt.py', '1\n2\n3\n')
    assert 'Too many wrong attempts' in out


@pytest.mark.parametrize('age, bill', [('15', 'Ghc20'), ('40', 'Ghc40'), ('50', 'Ghc0'), ('60', 'Ghc43')])
def test_rollercoaster_prices_every_age(age, bill):
    photo = 'y' if age == '60' else 'N'
    assert f'Your final bill is {bill}' in run('ask.py', f'150\n{age}\n{photo}\n')


def test_rollercoaster_too_short():
    assert 'at least 120cm' in run('ask.py', '110\n')


def test_pizza_accepts_lowercase_and_reasks_on_unknown_size():
    out = run('pizza_delivery_test.py', 'xl\nm\ny\nn\n')
    assert 'Choose a size: S, M or L' in out
    assert 'Your final bill is: $23.' in out


def test_bmi_accepts_decimals_and_centimetres():
    assert 'Your BMI is 23.0, you have a normal weight.' in run('bmi_calculator.py', '175\n70.5\n')


def test_leap_year_explains_itself():
    out = run('leap_year_checker.py', 'abc\n1900\n')
    assert 'Please type a year' in out
    assert 'It is not a leap year.' in out and 'not by 400' in out


def test_love_calculator():
    assert 'Your score is 53.' in run('love_calculator.py', 'Angela Yu\nJack Bauer\n')


def test_treasure_island_reasks_the_same_question():
    out = run('treasure_island_project.py', 'left\nwait\ngreen\nyellow\n')
    assert 'Please enter one of: Red, Blue, Yellow' in out
    assert out.strip().endswith('The treasure box is yours :)')
    assert out.count('Choose a path') == 1


def test_chemical_formula_rejects_a_malformed_formula_without_a_request():
    out = run('ChemicalFormula.py', 'hello\n')
    assert 'Enter a formula such as C6H6' in out
    assert out.count('Enter chemical formula') == 1      # it used to ask twice


def test_christmas_tree_draws_the_original_tree():
    out = run('ChristmasTree.py', '')
    assert out.splitlines()[0] == ' ' * 15 + '*'


def test_scripts_leave_quietly_on_ctrl_d():
    assert 'Bye!' in run('prompt.py', '')
