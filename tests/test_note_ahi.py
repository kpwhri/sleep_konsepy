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
    ('sleep study results performed on 01/01/2020 (AHI 30.5', 30.5),
])
def test_sm_ahi_all(text, exp):
    results = list(RUN_REGEXES_FUNC(text))
    if exp is None:
        assert len(results) == 0
    else:
        assert float(results[0]) == exp
