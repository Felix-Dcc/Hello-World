"""Body mass index."""

# (upper bound, key, how the result is described)
CATEGORIES = (
    (18.5, 'under', 'you are underweight'),
    (25, 'normal', 'you have a normal weight'),
    (30, 'over', 'you are slightly overweight'),
    (35, 'obese', 'you are obese'),
    (float('inf'), 'severe', 'you are clinically obese'),
)


def parse_height(text):
    """Height in metres. A value over 3 is taken as centimetres, since nobody
    is 3 m tall and 175 almost certainly means 175 cm."""
    value = float(text)
    if value > 3:
        value /= 100
    if not 0.5 <= value <= 2.75:
        raise ValueError('Enter a height between 0.5 and 2.75 m (50-275 cm)')
    return value


def parse_weight(text):
    value = float(text)
    if not 2 <= value <= 650:
        raise ValueError('Enter a weight between 2 and 650 kg')
    return value


def bmi(height_m, weight_kg):
    return weight_kg / height_m ** 2


def category(value):
    """(key, description) for a BMI value."""
    for upper, key, description in CATEGORIES:
        if value < upper:
            return key, description
