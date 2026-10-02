"""One view per project. All the rules live in projects/; these only parse
the form, call into it, and pick what to show.

Games and the ATM keep their state in Flask's session cookie and redirect
after each POST, so a page refresh never replays a move. The cookie is
signed, not encrypted: fine for a hangman word, not for real secrets.
"""
import string
from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from projects import (atm, bmi, chemistry, hangman, leap_year, love, password, pizza,
                      rollercoaster, rps, treasure_island, tree)

from .catalog import CATEGORIES, PROJECTS

bp = Blueprint('arcade', __name__)


def page(slug, **context):
    return render_template(f'{slug}.html', project=PROJECTS[slug], **context)


def whole(value, label, low, high):
    """A whole number from a form field, or a ValueError fit to show."""
    try:
        number = int(str(value).strip())
    except ValueError:
        raise ValueError(f'Enter {label} as a whole number.') from None
    if not low <= number <= high:
        raise ValueError(f'Enter {label} between {low} and {high}.')
    return number


@bp.get('/')
def hub():
    return render_template('hub.html', categories=CATEGORIES)


# -- Games ---------------------------------------------------------------------

HANGMAN_MESSAGES = {
    'hit': ('success', 'Yes! “{letter}” is in the word.'),
    'miss': ('error', 'No “{letter}”. You lose a life.'),
    'repeat': ('info', 'You’ve already guessed “{letter}”.'),
    'invalid': ('info', 'Guess a single letter from A to Z.'),
    'over': ('info', 'That game is over. Start a new one.'),
}


@bp.route('/hangman', methods=['GET', 'POST'])
def hangman_page():
    saved = session.get('hangman')
    game = hangman.Hangman.from_dict(saved) if saved else None
    if request.method == 'POST':
        if game is None or request.form.get('action') == 'new':
            game = hangman.Hangman.new()
        else:
            letter = request.form.get('letter', '')
            kind, message = HANGMAN_MESSAGES[game.guess(letter)]
            flash(message.format(letter=letter.strip().lower()), kind)
        session['hangman'] = game.to_dict()
        return redirect(url_for('.hangman_page'))

    if game is None:
        game = hangman.Hangman.new()
        session['hangman'] = game.to_dict()
    return page('hangman', game=game, alphabet=string.ascii_lowercase,
                max_lives=hangman.MAX_LIVES)


RPS_ICONS = {'rock': '✊', 'paper': '✋', 'scissors': '✌️'}
RPS_RESULTS = {'win': 'You win!', 'lose': 'Computer wins!', 'draw': 'It’s a draw!'}


@bp.route('/rock-paper-scissors', methods=['GET', 'POST'])
def rps_page():
    if request.method == 'POST':
        if request.form.get('action') == 'reset':
            session.pop('rps_score', None)
            session.pop('rps_last', None)
        else:
            player = request.form.get('choice', '')
            if player in rps.CHOICES:
                computer = rps.computer_choice()
                result = rps.outcome(player, computer)
                score = session.get('rps_score', {'win': 0, 'lose': 0, 'draw': 0})
                score[result] += 1
                session['rps_score'] = score
                session['rps_last'] = {'player': player, 'computer': computer, 'result': result}
            else:
                flash('Choose rock, paper or scissors.', 'error')
        return redirect(url_for('.rps_page'))

    return page('rps', choices=rps.CHOICES, icons=RPS_ICONS, results=RPS_RESULTS,
                score=session.get('rps_score', {'win': 0, 'lose': 0, 'draw': 0}),
                last=session.get('rps_last'))


@bp.route('/treasure-island', methods=['GET', 'POST'])
def treasure_island_page():
    state = session.get('treasure') or {'scene': treasure_island.START, 'path': []}
    if request.method == 'POST':
        if request.form.get('action') == 'restart':
            state = {'scene': treasure_island.START, 'path': []}
        else:
            answer = request.form.get('answer', '')
            try:
                state['scene'] = treasure_island.step(state['scene'], answer)
                state['path'].append(answer.strip().title())
            except ValueError as e:
                flash(str(e), 'error')
        session['treasure'] = state
        return redirect(url_for('.treasure_island_page'))

    scene = treasure_island.STORY[state['scene']]
    return page('treasure_island', scene=scene, path=state['path'],
                is_ending=isinstance(scene, treasure_island.Ending),
                banner=treasure_island.BANNER)


# -- Everyday tools ------------------------------------------------------------

@bp.route('/password', methods=['GET', 'POST'])
def password_page():
    values = {'letters': '12', 'symbols': '2', 'numbers': '2'}
    result = error = None
    if request.method == 'POST':
        values = {k: request.form.get(k, '').strip() for k in values}
        try:
            counts = {k: whole(v, f'the number of {k}', 0, password.MAX_PER_KIND)
                      for k, v in values.items()}
            bits = password.entropy_bits(**counts)
            result = {'password': password.generate(**counts), 'bits': bits,
                      'strength': password.strength(bits)}
        except ValueError as e:
            error = str(e)
    response = page('password', values=values, result=result, error=error,
                    max_per_kind=password.MAX_PER_KIND, symbols=password.SYMBOLS)
    # A generated password must not sit in a cache or be shared by Back/Forward.
    return response, {'Cache-Control': 'no-store'}


@bp.route('/bmi', methods=['GET', 'POST'])
def bmi_page():
    values = {'height': '', 'weight': ''}
    result = error = None
    if request.method == 'POST':
        values = {k: request.form.get(k, '').strip() for k in values}
        try:
            try:
                height, weight = float(values['height']), float(values['weight'])
            except ValueError:
                raise ValueError('Enter your height in cm and weight in kg as numbers.') from None
            value = bmi.bmi(bmi.parse_height(height), bmi.parse_weight(weight))
            key, description = bmi.category(value)
            result = {'value': value, 'key': key, 'description': description}
        except ValueError as e:
            error = str(e)
    return page('bmi', values=values, result=result, error=error)


@bp.get('/leap-year')
def leap_year_page():
    raw = request.args.get('year', '').strip()
    result = error = None
    if raw:
        try:
            year = whole(raw, 'a year', 1, 9999)
            result = {'year': year, 'leap': leap_year.is_leap(year),
                      'reason': leap_year.reason(year), 'next': leap_year.next_leap(year)}
        except ValueError as e:
            error = str(e)
    return page('leap_year', year=raw or str(date.today().year), result=result, error=error)


@bp.get('/chemistry')
def chemistry_page():
    formula = request.args.get('formula', '').strip()
    compound = error = None
    if formula:
        try:
            compound = chemistry.lookup(formula)
        except chemistry.LookupFailed as e:
            error = str(e)
    return page('chemistry', formula=formula, compound=compound, error=error,
                examples=['H2O', 'CO2', 'C6H6', 'C6H12O6', 'NaCl'])


# -- Shop and bank -------------------------------------------------------------

def fresh_atm():
    return {'attempts': 0, 'account': None}


@bp.route('/atm', methods=['GET', 'POST'])
def atm_page():
    state = session.get('atm') or fresh_atm()
    locked = state['attempts'] >= atm.MAX_PIN_ATTEMPTS
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'pin' and not locked and state['account'] is None:
            if atm.check_pin(request.form.get('pin', '')):
                state = {'attempts': 0, 'account': atm.Account().to_dict()}
                flash('Welcome! Your card is in.', 'success')
            else:
                state['attempts'] += 1
                left = atm.MAX_PIN_ATTEMPTS - state['attempts']
                flash(f'Wrong PIN. {left} attempt{"s" if left != 1 else ""} left.' if left
                      else 'Too many wrong attempts. Your card has been retained.', 'error')
        elif action in ('deposit', 'withdraw') and state['account'] is not None:
            account = atm.Account.from_dict(state['account'])
            try:
                amount = getattr(account, action)(request.form.get('amount', ''))
                done = 'Deposited' if action == 'deposit' else 'Withdrew'
                flash(f'{done} {atm.money(amount)}.', 'success')
            except atm.TransactionError as e:
                flash(str(e), 'error')
            data = account.to_dict()
            data['history'] = data['history'][-8:]      # keep the cookie small
            state['account'] = data
        elif action in ('exit', 'reset'):
            state = fresh_atm()
            if action == 'exit':
                flash('Card returned. Goodbye!', 'info')
        session['atm'] = state
        return redirect(url_for('.atm_page'))

    account = atm.Account.from_dict(state['account']) if state['account'] else None
    return page('atm', account=account, locked=locked, money=atm.money,
                attempts_left=atm.MAX_PIN_ATTEMPTS - state['attempts'], demo_pin=atm.DEMO_PIN)


@bp.get('/pizza')
def pizza_page():
    args = request.args
    order = error = None
    if 'size' in args:
        try:
            items, total = pizza.quote(args['size'], args.get('pepperoni') == 'on',
                                       args.get('cheese') == 'on')
            order = {'items': items, 'total': total}
        except ValueError as e:
            error = str(e)
    return page('pizza', args=args, order=order, error=error, sizes=pizza.SIZES,
                pepperoni=pizza.PEPPERONI, cheese=pizza.EXTRA_CHEESE)


def price_list():
    """Human labels for rollercoaster.TICKET_BANDS."""
    rows, low = [], 1
    for oldest, price in rollercoaster.TICKET_BANDS:
        ages = f'{low}+' if oldest is None else (f'Up to {oldest}' if low == 1 else f'{low}–{oldest}')
        rows.append((ages, f'GHS {price}' if price else 'Free'))
        low = (oldest or 0) + 1
    return rows


@bp.get('/rollercoaster')
def rollercoaster_page():
    args = request.args
    result = error = None
    if 'height' in args:
        try:
            height = whole(args['height'], 'your height in cm', 50, 250)
            age = whole(args['age'], 'your age', 1, 120) if args.get('age', '').strip() else None
            result = rollercoaster.quote(height, age, photo=args.get('photo') == 'on')
        except ValueError as e:
            error = str(e)
    return page('rollercoaster', args=args, result=result, error=error, prices=price_list(),
                min_height=rollercoaster.MIN_HEIGHT_CM, photo_price=rollercoaster.PHOTO_PRICE)


# -- Just for fun --------------------------------------------------------------

@bp.get('/love')
def love_page():
    name1 = request.args.get('name1', '').strip()
    name2 = request.args.get('name2', '').strip()
    result = error = None
    if 'name1' in request.args:
        if name1 and name2:
            score = love.love_score(name1, name2)
            result = {'score': score, 'verdict': love.verdict(score)}
        else:
            error = 'Enter both names.'
    return page('love', name1=name1, name2=name2, result=result, error=error)


@bp.get('/tree')
def tree_page():
    try:
        levels = whole(request.args.get('levels', '9'), 'the height', 3, 15)
    except ValueError:
        levels = 9
    lines = tree.christmas_tree(levels, margin=0).splitlines()
    return page('tree', levels=levels, leaves=lines[:levels], trunk=lines[levels:-1],
                pot=lines[-1])
