"""
Secure message patterns for AHI.
"""

import re
from enum import IntEnum

from konsepy.rxsearch import extract_first_regex_target, extract_all_regex_target

from sleep_konsepy.shared_patterns import DATE, is_not_overall_ahi, pre_find_impress, is_invalid_test_around, \
    has_date_prefix


class SmAhi(IntEnum):
    UNKNOWN = -1
    YES = 1


def pre_unattended_sleep_study_findings(text):
    if re.compile(r'UNATTENDED HOME SLEEP STUDY:').search(text):
        if m := re.compile(r'FINDINGS:.*IMPRESSION:', re.DOTALL).search(text):
            yield m.start(), m.end()
    return None


score = r'\b\d+(?:\.\d+)?\b'
target = rf'(?P<target>{score})'

of_is_at_was = r'(?:of|is|is\s*at|=|was|at)'
about = rf'(?:a\s*bout|approx\w+|only|less\s*than|(?:just\s*)?(?:over|under)|nearly|between\s*{score}\s*and)'
events = r'(?:apne\w*|pause|obstr\w*|respiratory|events|period|episode|interrupt|times|per\s*h(?:ou)?r|breathing)'

REGEXES = [
    (
        re.compile(r'\bPAHI\s*of\s*(?P<target>\d+(?:\.\d+)?)'),
        SmAhi.YES,
        None,
        pre_unattended_sleep_study_findings,
    ),
    (
        re.compile(rf'(?:an AHI of\s*|p?AHI\W*){target}', re.I),
        SmAhi.YES,
        [is_not_overall_ahi],
        pre_find_impress,
    ),
    (
        re.compile(
            rf'obstructive\s*sleep\s*apnea\W*(?:OSA\W*per|with\s*an?)\s*(?:baseline\s*)?p?AHI(?:\W*|\s*of\s*){target}',
            re.I,
        ),
        SmAhi.YES,
        [is_invalid_test_around, has_date_prefix],
    ),
    (
        re.compile(rf'overall\s*pahi\s*{of_is_at_was}\s*{target}'),
        SmAhi.YES,
        [has_date_prefix],
    ),
    (
        re.compile(
            r'\b('
            rf'{about}'
            r')\W*'
            rf'\W*{target}'
            r'(?:obstructive breathing events)',
            re.I,
        ),
        SmAhi.YES,
    ),
    (
        re.compile(
            rf'you\s+had\s+an\s+average\s+of\s+{about}?\s*{target}\W*{events}',
            re.I,
        ),
        SmAhi.YES,
        [is_invalid_test_around],
    ),
    (  # watchpat on 1/1/2001 (pahi 20.1)
        re.compile(
            r'(?:'
            rf'watchpat\W*'
            rf'(?:(?:on)\W+)*'
            rf'\W*{DATE}\W*pahi\W*{target}'
            r')',
            re.I,
        ),
        SmAhi.YES,
    ),
    (
        re.compile(
            r'\b('
            r'p?ahi'
            r'|(?:apnea|ahi)(?:\W*(?:an?|average|index|score|hypopnea|events?|rate))*'
            r'|(?:stopped\W*breathing|airway\W*close\s*s)\W*an\W*average'
            r')'
            r'[\s\-=:]*'
            r'(?:\(.*?\))?'
            r'[\s\-=:]*'
            rf'{of_is_at_was}?'
            r'[\s\-=:]*'
            rf'{target}'
            r'(?!-)'
            r'(?! to \d)'  # exclude range like 'AHI = 0 to 5'
            r'(?! t o \d)',  # exclude range like 'AHI = 0 to 5'
            re.I,
        ),
        SmAhi.YES,
        [is_not_overall_ahi, has_date_prefix],
    ),
]

RUN_REGEXES_FUNC = extract_first_regex_target(REGEXES)
# RUN_REGEXES_FUNC = extract_all_regex_target(REGEXES)
