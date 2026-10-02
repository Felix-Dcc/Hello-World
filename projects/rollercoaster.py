"""Rollercoaster eligibility and ticket price."""
from dataclasses import dataclass

MIN_HEIGHT_CM = 120
PHOTO_PRICE = 3

# Ticket price in GHS by age: (oldest age in the band, price). The original
# script only priced ages 20-35 and 45-55, so everyone else rode for GHS 0
# without being told why. The gaps now take the nearest band's price;
# edit this table to set real prices.
TICKET_BANDS = (
    (25, 20),
    (30, 30),
    (44, 40),
    (55, 0),      # 45-55 ride free
    (None, 40),
)


@dataclass
class Quote:
    can_ride: bool
    ticket: int = 0
    photo: int = 0

    @property
    def total(self):
        return self.ticket + self.photo


def ticket_price(age):
    for oldest, price in TICKET_BANDS:
        if oldest is None or age <= oldest:
            return price


def quote(height_cm, age=None, photo=False):
    if not 50 <= height_cm <= 250:
        raise ValueError('Enter a height between 50 and 250 cm')
    if height_cm < MIN_HEIGHT_CM:
        return Quote(can_ride=False)
    if age is None or not 1 <= age <= 120:
        raise ValueError('Enter an age between 1 and 120')
    return Quote(can_ride=True, ticket=ticket_price(age), photo=PHOTO_PRICE if photo else 0)
