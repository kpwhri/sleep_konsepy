"""
File for shared patterns (e.g., negation) to be used across concepts.
"""
import re

from konsepy.rxsearch import SKIP

not_overall_ahi_pat = re.compile(
    r'\b(?:'
    r'rem|supine|non\W*supine|prone|lateral|residual'
    r'|upright|sitting|central|sides?|back|non\W*back'
    r'|other\s*p\s?ositions?'
    r')\b',
    re.I,
)

invalid_test_pat = re.compile(
    r'(?:'
    r'\bmad\b'
    r'|\boat?\b'
    r'|\bdevice\b'
    r'|appliance'
    r'|therapy'
    r'|\bno\s+snore\b|dental\s+device'
    r'|\b(?:bi|c|a)pap\b'
    r')',
    re.I,
)

has_date_pat = re.compile(
    r'\b(?:(?:20|19)\d{2}|/\d{2}|previous|prior|last|ago)\b',
    re.I,
)


def has_date_prefix(*, m, text, postcontext, **_):
    if has_date_pat.search(text[max(0, m.start()-75):]):
        return SKIP
    elif has_date_pat.search(postcontext):
        return SKIP
    return None


def is_not_overall_ahi(*, precontext, **_):
    current_sentence = precontext.split('.')[-1]
    if not_overall_ahi_pat.search(current_sentence):
        return SKIP
    return None


def is_invalid_test_precontext(*, precontext, **_):
    return is_invalid_test(precontext)


def is_invalid_test_postcontext(*, postcontext, **_):
    return is_invalid_test(postcontext)


def is_invalid_test_around(*, around, **_):
    return is_invalid_test(around)


def is_invalid_test_around_500_window(*, m, text, **_):
    return is_invalid_test(text[max(0, m.start() - 200): m.end() + 100])


def is_invalid_test(text):
    if m := invalid_test_pat.search(text):
        return SKIP
    return None


MONTH = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b'
DATE = rf'(?:\d+/\W*\d+(?:/\W*\d+)?|\d+\W*{MONTH}(?:\W*\d+)?|{MONTH}\W*\d+(?:\W*\d+)?|\d+)'


def pre_find_impress(text):
    if m := re.compile(r'findings:.*?(?:impression|oxygen\s*saturation)', re.I | re.DOTALL).search(text):
        yield m.start(), m.end()
    return None
