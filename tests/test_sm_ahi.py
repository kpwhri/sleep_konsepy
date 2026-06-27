"""
Testing secure message patterns for AHI.
"""
import pytest

from sleep_konsepy.concepts.sm_ahi import RUN_REGEXES_FUNC


@pytest.mark.parametrize('text, exp', [
    ('UNATTENDED HOME SLEEP STUDY:\nFINDINGS:\nThis led to an overall PRDI of 20.5 and PAHI of 30.5.\nIMPRESSION:',
     30.5,
     ),
    ('overall pAHI of 30.5', 30.5),
    ('Baseline Apnea/Hypopnea Index (AHI) (which is the sleep apnea event rate) of 30.5 events per hour', 30.5),
    ('AHI = 0 to 5 Normal range', None),
    ('you had an average of about 20.1 apneas', 20.1),
    ('you had an average of between 20 and 21 apneas', 21),
    ('in 2000 with an AHI of 30.5 events per hour\nfindings:\n pAHI: >>> 20.1 events per hour\nimpression:', 20.1),
    ('findings:\npAHI:»»»20.1 events per hour\noxygen saturation:', 20.1),
    ('sleep apnea with a baseline AHI of 20.1 events per hour', 20.1),
])
def test_sm_ahi_all(text, exp):
    results = list(RUN_REGEXES_FUNC(text))
    if exp is None:
        assert len(results) == 0
    else:
        assert float(results[0]) == exp
