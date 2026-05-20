"""
Secure message patterns for AHI.
"""

import re
from enum import IntEnum

from konsepy.rxsearch import extract_first_regex_target


class SmAhi(IntEnum):
    UNKNOWN = -1
    YES = 1


def pre_unattended_sleep_study_findings(text):
    if re.compile(r'UNATTENDED HOME SLEEP STUDY:').search(text):
        if m := re.compile(r'FINDINGS:.*IMPRESSION:', re.DOTALL).search(text):
            yield m.start(), m.end()
    return None


of_is_at_was = r'(?:of|is|is\s*at|=|was|at)'
target = r'(?P<target>\d+(?:\.\d+)?)'

REGEXES = [
    (
        re.compile(r'PAHI\s*of\s*(?P<target>\d+(?:\.\d+)?)'),
        SmAhi.YES,
        None,
        pre_unattended_sleep_study_findings,
    ),
    (
        re.compile(rf'overall\s*pahi\s*{of_is_at_was}\s*{target}'),
        None,
    ),
    (
        re.compile(
            r'\b('
            r'p?ahi'
            r'|(?:apnea|ahi)(?:\W*(?:an?|average|index|score|hypopnea|events?|rate))*'
            r'|(?:stopped\W*breathing|airway\W*close\s*s)\W*an\W*average'
            r')'
            r'\W*'
            r'(?:\(.*?\))?'
            r'\W*'
            rf'{of_is_at_was}?'
            r'\W*'
            r'(?P<target>\d+(?:\.\d+)?)'
            r'(?! to \d)',  # exclude range like 'AHI = 0 to 5'
            re.I,
        ),
        SmAhi.YES,
    ),
    (
        re.compile(
            r'\b('
            r'about'
            r')\W*'
            r'\W*(?P<target>\d+(?:\.\d+)?)'
            r'(?:obstructive breathing events)?',
            re.I,
        ),
        SmAhi.YES,
    ),
]

RUN_REGEXES_FUNC = extract_first_regex_target(REGEXES)
