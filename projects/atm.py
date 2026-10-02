"""A demo cash machine. Money is Decimal, never float."""
import hmac
from decimal import Decimal, InvalidOperation

DEMO_PIN = '2050'
OPENING_BALANCE = Decimal('1000.00')
MAX_PIN_ATTEMPTS = 3
MAX_TRANSACTION = Decimal('1000000')
CENT = Decimal('0.01')


class TransactionError(ValueError):
    """A deposit or withdrawal that must not go through."""


def check_pin(entered, pin=DEMO_PIN):
    return hmac.compare_digest(str(entered).strip().encode(), pin.encode())


def money(amount):
    return f'GHS {amount:,.2f}'


def parse_amount(text):
    """A positive amount with at most two decimal places. Negative amounts
    are refused: the old version let a negative withdrawal add money."""
    try:
        amount = Decimal(str(text).strip().replace(',', ''))
    except InvalidOperation:
        raise TransactionError('Enter an amount such as 50 or 12.50') from None
    if not amount.is_finite():
        raise TransactionError('Enter an amount such as 50 or 12.50')
    if amount <= 0:
        raise TransactionError('Enter an amount greater than zero')
    if amount > MAX_TRANSACTION:
        raise TransactionError(f'The most you can move at once is {money(MAX_TRANSACTION)}')
    if amount != amount.quantize(CENT):
        raise TransactionError('Use at most two decimal places')
    return amount.quantize(CENT)


class Account:
    def __init__(self, balance=OPENING_BALANCE, history=()):
        self.balance = Decimal(balance)
        self.history = [tuple(entry) for entry in history]

    def deposit(self, amount):
        amount = parse_amount(amount)
        self.balance += amount
        self.history.append(('Deposit', str(amount), str(self.balance)))
        return amount

    def withdraw(self, amount):
        amount = parse_amount(amount)
        if amount > self.balance:
            raise TransactionError(f'Insufficient funds: your balance is {money(self.balance)}')
        self.balance -= amount
        self.history.append(('Withdrawal', str(amount), str(self.balance)))
        return amount

    def to_dict(self):
        return {'balance': str(self.balance), 'history': self.history}

    @classmethod
    def from_dict(cls, data):
        return cls(data['balance'], data['history'])
