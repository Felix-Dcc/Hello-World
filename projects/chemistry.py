"""Look up a compound on PubChem by its chemical formula."""
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from dataclasses import dataclass

FORMULA = re.compile(r'(?:[A-Z][a-z]?\d*)+')
TIMEOUT = 20          # seconds; pubchempy itself never times out


class LookupFailed(Exception):
    """Base class; the message is fit to show the user."""


class InvalidFormula(LookupFailed):
    pass


class NotFound(LookupFailed):
    pass


class Unavailable(LookupFailed):
    pass


@dataclass
class Compound:
    formula: str
    cid: int
    name: str            # IUPAC name; PubChem leaves it out for some compounds
    common_name: str     # first synonym, if PubChem lists any
    weight: str

    @property
    def url(self):
        return f'https://pubchem.ncbi.nlm.nih.gov/compound/{self.cid}'


def parse_formula(text):
    formula = re.sub(r'\s+', '', text)
    if not formula or len(formula) > 40 or not FORMULA.fullmatch(formula):
        raise InvalidFormula('Enter a formula such as C6H6 or H2O: element symbols '
                             'start with a capital letter.')
    return formula


def _search(formula):
    try:
        import pubchempy as pcp
    except ImportError:
        raise Unavailable('Lookups need pubchempy: pip install pubchempy') from None
    try:
        results = pcp.get_compounds(formula, 'formula')
        if not results:
            raise NotFound(f'No information found for {formula}. Please check the formula.')
        compound = results[0]
        synonyms = compound.synonyms or []      # a separate request; may be empty
        return Compound(formula, compound.cid, compound.iupac_name,
                        synonyms[0] if synonyms else None, str(compound.molecular_weight))
    except pcp.NotFoundError:
        raise NotFound(f'No information found for {formula}. Please check the formula.') from None
    except (pcp.PubChemHTTPError, OSError) as e:
        raise Unavailable("Couldn't reach PubChem just now. Check your connection "
                          'and try again.') from e


_pool = ThreadPoolExecutor(max_workers=2)


def lookup(text, search=_search, timeout=TIMEOUT):
    """The first compound PubChem lists for a formula, or a LookupFailed."""
    formula = parse_formula(text)
    future = _pool.submit(search, formula)
    try:
        return future.result(timeout=timeout)
    except FutureTimeout:
        raise Unavailable('PubChem took too long to answer. Try again in a moment.') from None
