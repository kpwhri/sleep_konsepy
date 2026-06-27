"""
Secure message patterns for AHI.
"""
import re
from enum import IntEnum

from konsepy.rxsearch import extract_first_regex_target

from sleep_konsepy.shared_patterns import is_not_overall_ahi, is_invalid_test_around, DATE, \
    is_invalid_test_around_500_window, pre_find_impress


class NoteAhi(IntEnum):
    UNKNOWN = -1
    YES = 1


score = r'\d+(?:\.\d+)?'
target = rf'(?P<target>{score})'

ahi = fr'(?:p?ahi|apno?ea\W*hypopnn?o?ea\W*index)'
per_hour = r'(?:events\s*)?(?:per\s*)?(?:hour|hr)'
of_is_at_was = r'(?:of|is|is\s*at|=|was|at)'
test_kind = r'(?:preliminary|home|bas\w+|medicare|molina|standard|(?:re\W*)?qualifying|follow\W*up|sleep\s*study)'
performed = r'(?:performed|completed)'
osa = r'(?:obstructive\s*sleep\s*apnea(?:\s*syndrome)|\bosa\b)'


def pre_watchpat_sleep_study(text):
    if re.compile(r'sleep\s*study', re.I).search(text):
        if m := re.compile(r'interpretation:.*?(?:recommendations|diagnosis):', re.I | re.DOTALL).search(text):
            yield m.start(), m.end()
        elif m := re.compile(r'interpretation:', re.I).search(text):
            yield m.end(), len(text)
        elif m := re.compile(r'(recommendations|diagnosis):', re.I).search(text):
            yield 0, m.start()
    return None


def pre_sumdx_recommend(text):
    if m := re.compile(r'summary\s*(?:and|&)\s*(?:diagnosis|conclusions?).*?recommendations?', re.I | re.DOTALL).search(
            text):
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


def home_unattended_sleep_study(text):
    if re.compile(r'home\s*unattended\s*sleep\s*study', re.I).search(text):
        yield 0, len(text)
    return None


REGEXES = [
    (
        re.compile(
            rf'(?:{test_kind}\W*)+sleep\W*study'
            rf'\W*(?:{performed}\W*)?with\W*the\W*watchpat\W*on\W*{DATE}\W*results\W*pAHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
    ),

    (
        re.compile(rf'apnea\s*hypopnea\s*index\s*\(AHI\):\s*{target}\s*events', re.I),
        NoteAhi.YES,
        None,
        [home_unattended_sleep_study],
    ),
    (
        re.compile(
            rf'\W*(?:{performed}\W*)?with\W*the\W*watchpat\W*'
            rf'(?:on\W*)?(?:{DATE}\W*)?'
            rf'(?:with\s*)?(?:baseline\W*)?(?:results\W*)?p?AHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
    ),
    (
        re.compile(
            rf'(?:{test_kind}\W*)+watchpat\W*(?:sleep\W*study\W*results\W*)'
            rf'(?:{performed}\W*)?on\W*(?:{DATE}\W*)?p?AHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
    ),
    (
        re.compile(
            rf'watchpat\s*study\s*reported\s*an?\s*{ahi}\s*{of_is_at_was}\s*{target}\s*{per_hour}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
    ),
    (
        re.compile(
            rf'sleep\W*study\W*results'
            rf'\W*(?:{performed}\W*)?on\W*{DATE}\W*p?AHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
    ),
    (
        re.compile(
            rf'obstructive\s*sleep\s*apnea\W*(?:OSA\W*per|with\s*an?)\s*(?:baseline\s*)?p?AHI(?:\W*|\s*of\s*){target}',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
    ),
    (
        re.compile(
            rf'indication:\s*(?:mild|moderate|severe)\s*{osa}\s*\(ahi\s*{target}\)',
            re.I,
        ),
        NoteAhi.YES,
        [is_invalid_test_around],
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
        # exclude 3%
        re.compile(rf'the\s*pAHI\s*(?:4%\s*)?(?:was|is)\s*{target}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_watchpat_sleep_study,
    ),
    (
        re.compile(
            rf'sleep\s*summary\s*'
            rf'start\s*time\W*\d+:\d+\s*'
            rf'end\s*time\W*\d+:\d+\s*'
            rf'PAHI\W*{target}',
            re.I,
        ),
        NoteAhi.YES,
    ),
    (
        re.compile(rf'with\s*pAHI\s*of\s*{target}'),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_sumdx_recommend,
    ),
    (
        re.compile(rf'(?:an AHI of\s*|p?AHI\W*){target}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_find_impress,
    ),
    (
        re.compile(rf'p?AHI\s*(?:on\s*this\s*test\s*)?(?:{of_is_at_was}\s*)?{target}'),
        NoteAhi.YES,
        [is_not_overall_ahi],
        pre_impress_recommend,
    ),
    (
        re.compile(rf'respiratory\s*indices\W*(?:summary\W*)?pahi[\s:]*{target}', re.I),
        NoteAhi.YES,
    ),
    (
        re.compile(rf'\bp?ahi\W*{target}\W*{per_hour}', re.I),
        NoteAhi.YES,
        [is_not_overall_ahi],
    ),
    (
        re.compile(
            rf'overall\s*(?:(?:normal|mild|moderate|severe|elevated|4%)\w*\s*)*{ahi}\s+{of_is_at_was}\s*{target}',
            re.I),
        NoteAhi.YES,
    ),
    (
        re.compile(
            rf'overall\s*{ahi}\s*'
            rf'(?:(?:on\s*this\s*study|is|still|normal|mild|moderate|severe|elevated|4%)\w*\s*)*'
            rf'{of_is_at_was}\s*{target}',
            re.I),
        NoteAhi.YES,
    ),
    (
        re.compile(rf'overall\s*{ahi}\s+(?:\w+\s+){{,10}}{target}\W*{per_hour}', re.I),
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
    (
        re.compile(
            rf'p?AHI\s*{target}\s*\('
            rf'(?:'
            rf'(?:p?AHI\s*)?\d+(?:\.\d+)?\s*supine'
            rf'|supine\s*(?:pahi\s*)?\d+(?:\.\d+)?'
            rf')',
            re.I),
        NoteAhi.YES,
        [is_invalid_test_around_500_window],
    ),
]

RUN_REGEXES_FUNC = extract_first_regex_target(REGEXES)
