from projects.chemistry import LookupFailed, lookup
from terminal import run


def main():
    formula = input('Enter chemical formula: ')
    try:
        compound = lookup(formula)
    except LookupFailed as e:
        print(e)
        return

    print(f'Name: {compound.name or "(no IUPAC name listed)"}')
    print(f'Common Name: {compound.common_name or "(none listed)"}')
    print(f'Molecular Weight: {compound.weight}')
    print(f'More: {compound.url}')


if __name__ == '__main__':
    run(main)
