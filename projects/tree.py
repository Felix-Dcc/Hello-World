"""An ASCII Christmas tree, without numpy."""


def christmas_tree(levels=9, margin=7):
    """The defaults draw exactly what ChristmasTree.py always printed."""
    if not 1 <= levels <= 30:
        raise ValueError('Choose a tree between 1 and 30 levels tall')
    centre = margin + levels - 1                     # column of the top star
    rows = [' ' * (centre - i) + '*' * (2 * i + 1) for i in range(levels)]
    rows += [' ' * centre + '|| '] * 3                # trunk
    rows.append(' ' * (centre - 2) + '\\=======/')    # pot
    return '\n'.join(rows)
