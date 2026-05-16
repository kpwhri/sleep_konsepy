"""
File for shared patterns (e.g., negation) to be used across concepts.
"""
import re

from konsepy.rxsearch import SKIP

not_overall_ahi_pat = re.compile(
    r'(?:'
    r'rem|supine|non\W*supine|prone|lateral|residual'
    r'|upright|sitting|central|obstructive'
    r')',
    re.I,
)


def is_not_overall_ahi(*, precontext, **_):
    current_sentence = precontext.split('.')[-1]
    if not_overall_ahi_pat.search(current_sentence):
        return SKIP
    return None
