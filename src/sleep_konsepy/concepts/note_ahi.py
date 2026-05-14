"""
Secure message patterns for AHI.
"""

# TODO: prenegation: supine, residual?, REM AHI

import re
from enum import IntEnum

from konsepy.rxsearch import extract_first_regex_target


class NoteAhi(IntEnum):
    UNKNOWN = -1


target = r'(?P<target>\d+(?:\.\d+)?)'
per_hour = r'(?:events\s*)?(?:per\s*)?(?:hour|hr)'
of_is_at_was = r'(?:of|is|is\s*at|=|was|at)'


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
        re.compile(rf'p rdi p ahi.*?\d+(?:\.\d+)?\s*{target}', re.I | re.DOTALL),
        None,
        None,
        pre_res_oxysat,
    ),
    (
        re.compile(rf'The pAHI was {target}'),
        None,
        None,
        pre_watchpat_sleep_study,
    ),
    (
        re.compile(rf'with\s*pAHI\s*of\s*{target}'),
        None,
        None,
        pre_sumdx_recommend,
    ),
    (
        re.compile(rf'(?:an AHI of|pAHI\W*)\s*{target}', re.I),
        None,
        None,
        pre_find_impress,
    ),
    (
        re.compile(rf'p?AHI\s*(?:{of_is_at_was}\s*)?{target}'),
        None,
        None,
        pre_impress_recommend,
    ),
    (
        re.compile(rf'respiratory\s*indices\s*pahi\s*{target}', re.I),
        None,
    ),
    (
        re.compile(rf'\bp?ahi\W*{target}\W*{per_hour}', re.I),
        None,
    ),
    (
        re.compile(rf'overall\s*p?ahi\s+(?:\w+\s+){{,10}}{target}\W*{per_hour}', re.I),
        None,
    ),
    (
        re.compile(rf'overall\s*p?ahi\s+{of_is_at_was}\s*{target}', re.I),
        None,
    ),
    (
        re.compile(rf'sleep\s*study\s*results\s*performed.*?AHI\s*{target}', re.I),
        None,
    ),
]

RUN_REGEXES_FUNC = extract_first_regex_target(REGEXES)
