"""Python Pizza Deliveries: price an order."""

SIZES = {'S': ('Small', 15), 'M': ('Medium', 20), 'L': ('Large', 25)}
PEPPERONI = {'S': 2, 'M': 3, 'L': 3}
EXTRA_CHEESE = 1


def parse_size(text):
    """'S', 'M' or 'L', from any case or the full word."""
    value = text.strip().upper()
    for key, (name, _) in SIZES.items():
        if value in (key, name.upper()):
            return key
    raise ValueError('Choose a size: S, M or L')


def quote(size, pepperoni=False, cheese=False):
    """Line items and total. An unknown size is an error: the old version
    billed it as a free pizza and still charged for the toppings."""
    size = parse_size(size)
    name, price = SIZES[size]
    items = [(f'{name} pizza', price)]
    if pepperoni:
        items.append(('Pepperoni', PEPPERONI[size]))
    if cheese:
        items.append(('Extra cheese', EXTRA_CHEESE))
    return items, sum(p for _, p in items)
