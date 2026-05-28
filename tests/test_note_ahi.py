"""
Testing secure message patterns for AHI.
"""
import pytest

from sleep_konsepy.concepts.note_ahi import RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('Respiratory Indices\npAHI 30.5\nODI 20.5', 30.5,),
    ('Summary & Diagnosis:\nPatient\'s study demonstrates sleep apnea with pAHI of 30 wich was associated\nRecommendations:', 30),
    ('Apneas + hypopneas (AHI) >> 30.5 per hour', 30.5),
    ('Results:\np rdi p ahi\n10.2 30.5\nOxygen Saturation', 30.5),
    ('Overall AHI is at the blah blah blah 30.5/hr', 30.5),
    ('follow-up sleep study results performed on 01/01/2020 (AHI 30.5', 30.5),
    ('The patient\'s Apnea/Hypopnea index is 30.5 per hour.', 30.5),
    ('preliminary home sleep study performed with the WatchPAT on 01/01/2020 results (pAHI 30.5 (pAHI 5 supine',
     30.5),
    ('preliminary baseline sleep study performed with the WatchPAT on 1/1/2020 results (pAHI 30.5 (pAHI 5 supine',
     30.5),
    ('baseline WatchPat sleep study results completed on 1/1/20. pAHI 30.5 (5supine', 30.5),
    ('medicare baseline WatchPat sleep study results completed on January 1, 2020. pAHI 30.5 (5supine',
     30.5),
    ('Preliminary WatchPat sleep study results completed on Jan 01, 2020. pAHI 30.5',
     30.5),
    ('led to an overall PRDI of 5.0 and PAHI of 30.5', 30.5),
    ('overall apnea/hypopnea index of 30.5', 30.5),
])
def test_note_ahi_all(text, exp):
    results = list(RUN_REGEXES_FUNC(text))
    if exp is None:
        assert len(results) == 0
    else:
        assert float(results[0]) == exp, f'Expected: {exp}, Got: {results}'
