"""
Testing secure message patterns for AHI.
"""
import pytest

from sleep_konsepy.concepts.note_ahi import RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('Respiratory Indices\npAHI 30.5\nODI 20.5', 30.5,),
    ('Summary & Diagnosis:\nPatient\'s study demonstrates sleep apnea with pAHI of 30 wich was associated\nRecommendations:',
     30),
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
    ('Preliminary baseline sleep study performed with the WatchPAT on 1/1/2001 (pAHI 20.1 (25.3 supine)', 20.1),
    ('performed with the WatchPAT on 1/1/2001 while on MAD results (pAHI 20.1 (25.3 supine)', None),
    ('performed with the WatchPAT on 01012001 results (pAHI 20.1 (25.3 supine)', 20.1),
    ('performed with the WatchPAT on results (pAHI 20.1 (25.3 supine)', 20.1),
    ('performed with the WatchPAT on (AHI 20.1 (25.3 supine)', 20.1),
    ('pAHI 20.1 (supine pAHI 25.3)', 20.1),
    ('Preliminary baseline (with MAD) sleep study performed with the WatchPAT on 1/1/2001 results (pAHI 20.1', None),
    ('performed with the WatchPAT on results (pAHI 20.1 (pAHI 25.3 supine', 20.1),
    ('Preliminary baseline (with oral appliance therapy) sleep study performed with the WatchPAT on 1/1/2001 results (pAHI 20.1',
     None),
    ('Respiratory indices\nPAHI 20.1\nODI 25.3', 20.1),
    ('Respiratory indices:\nPAHI 20.1\nODI 25.3', 20.1),
    ('Impression:\nThis patient has severe obstructive sleep apnea with pAHI 20.1\nPlan:', 20.1),
    ('blah blah pAHI 20.1 (25.3 supine for', 20.1),
    ('Indication: Mild OSA (AHI 20.1)', 20.1),
    ('Indication: Mild Obstructive Sleep Apnea Syndrome (AHI 20.1)', 20.1),
    ('moderate Obstructive Sleep Apnea (OSA), per baseline pAHI 20.1', 20.1),
    ('sleep study\ninterpretation:\nthe pAHI was 20.1 indicating moderate sleep apnea\nrecommendations:\n', 20.1),
    ('sleep study\ninterpretation:\nthe pAHI 4% was 20.1 indicating moderate sleep apnea\nrecommendations:\n', 20.1),
    ('sleep summary\nstart time: 20:01\nend time: 10:02\nPAHI: 20.1\nODI: 25.3', 20.1),
    ('home unattended sleep study\nApnea hypopnea index (AHI): 20.1 events/hour\nOD: 25.3', 20.1),
    ('overall normal pAHI of 20.1', 20.1),
    ('findings:\n pAHI: >>> 20.1 events per hour\nimpression:', 20.1),
    ('overall mildly elevated pAHI of 20.1', 20.1),
])
def test_note_ahi_all(text, exp):
    results = list(RUN_REGEXES_FUNC(text))
    if exp is None:
        assert len(results) == 0
    else:
        assert float(results[0]) == exp, f'Expected: {exp}, Got: {results}'
