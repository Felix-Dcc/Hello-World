"""The web UI, through Flask's test client."""
from html import unescape
import re

import pytest

from arcade import create_app
from arcade.catalog import PROJECTS
from projects import chemistry


@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SECRET_KEY': 'test'})
    return app.test_client()


def text(response):
    return response.get_data(as_text=True)


# -- Every page ----------------------------------------------------------------

def test_hub_links_to_every_project(client):
    html = text(client.get('/'))
    for project in PROJECTS.values():
        assert project.title in html
    links = set(re.findall(r'class="card project-card" href="([^"]+)"', html))
    assert len(links) == len(PROJECTS) == 12
    for link in links:
        response = client.get(link)
        assert response.status_code == 200, link
        assert 'Prefer the terminal?' in text(response)


def test_security_headers(client):
    headers = client.get('/').headers
    csp = headers['Content-Security-Policy']
    assert "script-src 'self'" in csp and "'unsafe-inline'" not in csp
    assert headers['X-Content-Type-Options'] == 'nosniff'


def test_no_inline_scripts_or_styles_anywhere(client):
    # The CSP forbids them, so any that crept in would silently not work.
    hub = text(client.get('/'))
    for link in ['/'] + re.findall(r'class="card project-card" href="([^"]+)"', hub):
        html = text(client.get(link))
        assert ' style=' not in html, link
        assert not re.search(r'\son[a-z]+=', html), link
        assert not re.search(r'<script(?![^>]*\bsrc=)', html), link


# -- Hangman -------------------------------------------------------------------

def start_hangman(client, word):
    with client.session_transaction() as s:
        s['hangman'] = {'word': word, 'lives': 6, 'guessed': []}


def test_hangman_does_not_reveal_the_word_while_playing(client):
    start_hangman(client, 'zephyr')
    html = text(client.get('/hangman'))
    assert 'zephyr' not in html.lower()
    assert 'The word so far: _ _ _ _ _ _' in html


def test_hangman_hit_miss_repeat(client):
    start_hangman(client, 'zephyr')
    html = text(client.post('/hangman', data={'letter': 'e'}, follow_redirects=True))
    assert '“e” is in the word' in html
    html = text(client.post('/hangman', data={'letter': 'q'}, follow_redirects=True))
    assert 'No “q”' in html and 'aria-label="5 of 6 lives left"' in html
    html = text(client.post('/hangman', data={'letter': 'q'}, follow_redirects=True))
    assert 'already guessed “q”' in html and 'aria-label="5 of 6 lives left"' in html
    html = text(client.post('/hangman', data={'letter': 'ab'}, follow_redirects=True))
    assert 'single letter' in html


def test_hangman_win_and_play_again(client):
    start_hangman(client, 'ivy')
    for letter in 'ivy':
        html = text(client.post('/hangman', data={'letter': letter}, follow_redirects=True))
    assert 'You win!' in html and 'Play again' in html
    html = text(client.post('/hangman', data={'action': 'new'}, follow_redirects=True))
    assert 'You win!' not in html and 'lives left' in html


def test_hangman_loss_shows_the_word(client):
    start_hangman(client, 'ivy')
    for letter in 'abcdef':
        html = text(client.post('/hangman', data={'letter': letter}, follow_redirects=True))
    assert 'Out of lives' in html and '<strong>ivy</strong>' in html


# -- Rock, paper, scissors -----------------------------------------------------

def test_rps_plays_a_round_and_keeps_score(client, monkeypatch):
    monkeypatch.setattr('projects.rps.computer_choice', lambda: 'scissors')
    html = text(client.post('/rock-paper-scissors', data={'choice': 'rock'}, follow_redirects=True))
    assert 'You win!' in html and 'Computer: Scissors' in html
    html = text(client.post('/rock-paper-scissors', data={'choice': 'paper'}, follow_redirects=True))
    assert 'Computer wins!' in html
    assert re.search(r'<dt>You</dt><dd>1</dd>.*<dt>Computer</dt><dd>1</dd>', html, re.S)
    html = text(client.post('/rock-paper-scissors', data={'action': 'reset'}, follow_redirects=True))
    assert re.search(r'<dt>You</dt><dd>0</dd>', html)


def test_rps_rejects_unknown_move(client):
    html = text(client.post('/rock-paper-scissors', data={'choice': 'lizard'}, follow_redirects=True))
    assert 'Choose rock, paper or scissors.' in html


# -- Treasure Island -----------------------------------------------------------

def test_treasure_island_win_with_a_wrong_turn(client):
    for answer in ('left', 'wait', 'green'):
        html = text(client.post('/treasure-island', data={'answer': answer}, follow_redirects=True))
    assert 'Please enter one of: Red, Blue, Yellow' in html and 'Which door?' in html
    html = text(client.post('/treasure-island', data={'answer': 'yellow'}, follow_redirects=True))
    assert 'The treasure box is yours' in html and 'Left → Wait → Yellow' in html
    html = text(client.post('/treasure-island', data={'action': 'restart'}, follow_redirects=True))
    assert 'Choose a path. Left or Right?' in html


# -- Password ------------------------------------------------------------------

def test_password_generates_the_mix_and_is_not_cached(client):
    response = client.post('/password', data={'letters': '20', 'symbols': '10', 'numbers': '11'})
    escaped = re.search(r'id="generated" class="mono big-input" value="([^"]+)"', text(response)).group(1)
    password = unescape(escaped)       # & arrives as &amp;, as it should
    assert len(password) == 41
    assert response.headers['Cache-Control'] == 'no-store'
    assert 'Very strong' in text(response)


@pytest.mark.parametrize('form, message', [
    ({'letters': 'x', 'symbols': '1', 'numbers': '1'}, 'Enter the number of letters as a whole number.'),
    ({'letters': '0', 'symbols': '0', 'numbers': '0'}, 'Ask for at least one character'),
    ({'letters': '99', 'symbols': '0', 'numbers': '0'}, 'between 0 and 50'),
])
def test_password_reports_bad_counts(client, form, message):
    html = text(client.post('/password', data=form))
    assert message in html and 'id="generated"' not in html


# -- BMI, leap year, chemistry -------------------------------------------------

def test_bmi(client):
    html = text(client.post('/bmi', data={'height': '175', 'weight': '70.5'}))
    assert 'Your BMI is 23.0: you have a normal weight.' in html
    html = text(client.post('/bmi', data={'height': 'tall', 'weight': '70'}))
    assert 'as numbers' in html
    html = text(client.post('/bmi', data={'height': '20', 'weight': '70'}))
    assert 'Enter a height between' in html


def test_leap_year(client):
    html = text(client.get('/leap-year?year=1900'))
    assert '1900 is not a leap year' in html and 'not by 400' in html
    assert 'The next leap year is 1904' in html
    assert 'Enter a year between 1 and 9999' in text(client.get('/leap-year?year=0'))


def test_chemistry_shows_a_compound(client, monkeypatch):
    found = chemistry.Compound('C6H6', 241, 'benzene', 'Benzene', '78.11')
    monkeypatch.setattr(chemistry, 'lookup', lambda f: found)
    html = text(client.get('/chemistry?formula=C6H6'))
    assert '78.11 g/mol' in html and 'https://pubchem.ncbi.nlm.nih.gov/compound/241' in html


def test_chemistry_shows_errors(client, monkeypatch):
    def offline(formula):
        raise chemistry.Unavailable("Couldn't reach PubChem just now.")
    monkeypatch.setattr(chemistry, 'lookup', offline)
    assert "Couldn&#39;t reach PubChem" in text(client.get('/chemistry?formula=H2O'))
    monkeypatch.undo()
    assert 'Enter a formula such as C6H6' in text(client.get('/chemistry?formula=hello'))


# -- ATM -----------------------------------------------------------------------

def test_atm_full_session(client):
    html = text(client.get('/atm'))
    assert 'the PIN is 2050' in html
    html = text(client.post('/atm', data={'action': 'pin', 'pin': '2050'}, follow_redirects=True))
    assert 'GHS 1,000.00' in html
    html = text(client.post('/atm', data={'action': 'deposit', 'amount': '250.50'}, follow_redirects=True))
    assert 'Deposited GHS 250.50.' in html and 'GHS 1,250.50' in html
    html = text(client.post('/atm', data={'action': 'withdraw', 'amount': '-500'}, follow_redirects=True))
    assert 'greater than zero' in html and 'GHS 1,250.50' in html
    html = text(client.post('/atm', data={'action': 'withdraw', 'amount': '5000'}, follow_redirects=True))
    assert 'Insufficient funds' in html
    html = text(client.post('/atm', data={'action': 'exit'}, follow_redirects=True))
    assert 'Card returned' in html and 'Insert your card' in html


def test_atm_locks_after_three_wrong_pins_and_ignores_more(client):
    for _ in range(3):
        html = text(client.post('/atm', data={'action': 'pin', 'pin': '0000'}, follow_redirects=True))
    assert 'Card retained' in html
    html = text(client.post('/atm', data={'action': 'pin', 'pin': '2050'}, follow_redirects=True))
    assert 'Card retained' in html and 'Available balance' not in html
    html = text(client.post('/atm', data={'action': 'reset'}, follow_redirects=True))
    assert 'Insert your card' in html


def test_atm_needs_a_pin_before_moving_money(client):
    client.post('/atm', data={'action': 'deposit', 'amount': '10'})
    with client.session_transaction() as s:
        assert s['atm']['account'] is None


# -- Pizza, rollercoaster ------------------------------------------------------

def test_pizza(client):
    html = text(client.get('/pizza?size=m&pepperoni=on'))
    assert 'Medium pizza' in html and '$23' in html
    assert 'Choose a size' in text(client.get('/pizza?size=XL'))


@pytest.mark.parametrize('query, expected', [
    ('height=150&age=40&photo=on', 'GHS 43'),
    ('height=150&age=50', 'Free'),
    ('height=110', 'at least 120 cm'),
    ('height=150&age=abc', 'Enter your age as a whole number.'),
    ('height=150', 'Enter an age between 1 and 120'),
])
def test_rollercoaster(client, query, expected):
    assert expected in text(client.get(f'/rollercoaster?{query}'))


def test_rollercoaster_price_list_matches_the_bands(client):
    html = text(client.get('/rollercoaster'))
    for label in ('Up to 25', '26–30', '31–44', '45–55', '56+'):
        assert label in html


# -- Love, tree ----------------------------------------------------------------

def test_love_calculator_escapes_names(client):
    html = text(client.get('/love?name1=Angela+Yu&name2=Jack+Bauer'))
    assert 'your score is 53' in html
    html = text(client.get('/love?name1=<script>alert(1)</script>&name2=x'))
    assert '<script>alert(1)' not in html and '&lt;script&gt;' in html
    assert 'Enter both names.' in text(client.get('/love?name1=Ada&name2='))


def test_tree_heights(client):
    html = text(client.get('/tree?levels=5'))
    assert html.count('class="tree-leaves"') == 4 and html.count('class="tree-star"') == 1
    assert 'value="9"' in text(client.get('/tree?levels=banana'))
