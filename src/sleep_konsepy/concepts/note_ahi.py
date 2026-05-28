"""
Secure message patterns for AHI.
"""
import re
from enum import IntEnum

from konsepy.rxsearch import extract_first_regex_target

from sleep_konsepy.shared_patterns import is_not_overall_ahi, is_invalid_test_precontext


class NoteAhi(IntEnum):
    UNKNOWN = -1
    YES = 1


score = r'\d+(?:\.\d+)?'
target = rf'(?P<target>{score})'

ahi = fr'(?:p?ahi|apno?ea\W*hypopnn?o?ea\W*index)'
per_hour = r'(?:events\s*)?(?:per\s*)?(?:hour|hr)'
of_is_at_was = r'(?:of|is|is\s*at|=|was|at)'
test_kind = r'(?:preliminary|home|bas\w+|medicare|molina|standard|(?:re\W*)?qualifying|follow\W*up)'
month = r'\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b'
performed = r'(?:performed|completed)'

date = rf'(?:\d+/\W*\d+(?:/\W*\d+)?|\d+\W*{month}(?:\W*\d+)?|{month}\W*\d+(?:\W*\d+)?)'


def pre_watchpat_sleep_study(text):
    if re.compile(r'watchpat\s*sleep\s*study\s*summary\s*and\s*interpretation', re.I).search(text):
        if m := re.compile(r'interpretation:.*?recommendations:', re.I | re.DOTALL).search(text):
            yield m.start(), m.end()
    return None


def pre_sumdx_recommend(text):
    if m := re.compile(r'summary\s*(?:and|&)\s*(?:diagnosis|conclusions?).*?recommendations?', re.I | re.DOTALL).search(
            text):
        yield m.start(), m.end()
    return None


def pre_find_impress(text):
    if m := re.compile(r'findings:.*?impression', re.I | re.DOTALL).search(text):
        yield m.start(), m.end()
    return None


def pre_impress_recommend(text):
    if m := re.compile(r'impression:.*?(?:recommendations?|plan)', re.I | re.DOTALL).search(text):
        yield m.start(), m.end()
    return None


def pre_res_oxysat(text):
    if m := re.compile(r'results:.*?oxygen\s*saturation', re.I | re.DOTALL).search(text):
        yield m.start(), m.end()
    return None


REGEXES = [
    (
        re.compile(
            rf'(?:{test_kind}\W*)+sleep\W*study'
            rf'\W*(?:{performed}\W*)?with\W*the\W*watchpat\W*on\W*{date}\W*results\W*pAHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_precontext],
    ),
    (
        re.compile(
            rf'\W*(?:{performed}\W*)?with\W*the\W*watchpat\W*on\W*{date}\W*results\W*p?AHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_precontext],
    ),
    (
        re.compile(
            rf'(?:{test_kind}\W*)+watchpat\W*sleep\W*study\W*results'
            rf'\W*(?:{performed}\W*)?on\W*{date}\W*p?AHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_precontext],
    ),
    (
        re.compile(
            rf'sleep\W*study\W*results'
            rf'\W*(?:{performed}\W*)?on\W*{date}\W*p?AHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_precontext],
    ),
    (
        re.compile(
            rf'(?:overall|total)\W*prdi\W*of\W*{score}\W*and\W*pahi\W*of\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
    ),
    (
        re.compile(rf'p rdi p ahi.*?\d+(?:\.\d+)?\s*{target}', re.I | re.DOTALL),
        NoteAhi.YES,
        None,
        pre_res_oxysat,
    ),
    (
        re.compile(rf'The pAHI was {target}'),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_watchpat_sleep_study,
    ),
    (
        re.compile(rf'with\s*pAHI\s*of\s*{target}'),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_sumdx_recommend,
    ),
    (
        re.compile(rf'(?:an AHI of|p?AHI\W*)\s*{target}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_find_impress,
    ),
    (
        re.compile(rf'p?AHI\s*(?:{of_is_at_was}\s*)?{target}'),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_impress_recommend,
    ),
    (
        re.compile(rf'respiratory\s*indices\s*pahi\s*{target}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
    ),
    (
        re.compile(rf'\bp?ahi\W*{target}\W*{per_hour}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
    ),
    (
        re.compile(rf'overall\s*{ahi}\s+(?:\w+\s+){{,10}}{target}\W*{per_hour}', re.I),
        NoteAhi.YES,
    ),
    (
        re.compile(rf'overall\s*{ahi}\s+{of_is_at_was}\s*{target}', re.I),
        NoteAhi.YES,
    ),
    (
        re.compile(rf'apnea/hypopnea\W*index\W*is\W*{target}\W*{per_hour}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
    ),
    (
        re.compile(rf'correction\W*p?ahi\W*{target}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
    ),
]

RUN_REGEXES_FUNC = extract_first_regex_target(REGEXES)
