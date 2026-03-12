import pytest

from sleep_konsepy.concepts.ahi import AHI3_PAT, AHI4_PAT, AHI_PAT
from utils import check_pattern


@pytest.mark.parametrize('sentence, expected_val', [
    ('AHI3%: 15.5', '15.5'),
    ('pAHI3%: 10.2', '10.2'),
    ('Total AHI3%: 12.0', '12.0'),
    ('AHI3% = 8.5', '8.5'),
    ('AHI3% 20.1', '20.1'),
    ('AHI 3% 14.2/hr', '14.2'),
    ('AHI (3%) 7.5', '7.5'),
    ('AHI 3% 10.0 / 4% 8.0', '10.0'),
    ('AHI 4% 8.0 / 3% 10.0', '10.0'),
    ('AHI 3% of 5.5/hour', '5.5'),
])
def test_ahi3_patterns(sentence, expected_val):
    assert check_pattern(sentence, expected_val, AHI3_PAT)


@pytest.mark.parametrize('sentence, expected_val', [
    ('AHI4%: 12.5', '12.5'),
    ('pAHI4%: 11.2', '11.2'),
    ('Total AHI4%: 15.0', '15.0'),
    ('AHI4% = 9.8', '9.8'),
    ('AHI4% 18.2', '18.2'),
    ('AHI 4% 14.5/hr', '14.5'),
    ('AHI (4%) 7.0', '7.0'),
    ('AHI 3% 10.0/4% 12.5', '12.5'),
    ('AHI 4% of 11.0/hour', '11.0'),
])
def test_ahi4_patterns(sentence, expected_val):
    assert check_pattern(sentence, expected_val, AHI4_PAT)


@pytest.mark.parametrize('sentence, expected_val', [
    ('AHI: (total) :: 25.4 events/hour', '25.4'),
    ('AHI: (total) 30.0 events/hour', '30.0'),
    ('Overall AHI: 18.5 per hour', '18.5'),
    ('Overall AHI: 15.0', '15.0'),
    ('Total AHI: 22.1 per hour', '22.1'),
    ('Total AHI: 19.5 per hr', '19.5'),
    ('pAHI: 14.8', '14.8'),
    ('AHI of 11.2', '11.2'),
    ('AHI was 9.5 events/hr', '9.5'),
    ('Apnea-Hypopnea Index (AHI): 28.3 per hour', '28.3'),
    ('Apnea / Hypopnea Index 24.0', '24.0'),
    ('AHI= 16.5 per', '16.5'),
    ('apnea-hypopnea index was 12.5 per hour', '12.5'),
    ('AHI: 14.0 events / hour', '14.0'),
    ('Apnea/Hypopnea Index (AHI) of 13.5 events/hour', '13.5'),
    ('(AHI) of 10.0 events per hour', '10.0'),
    ('(AHI) of 8.5', '8.5'),
    ('PSG AHI 17.2', '17.2'),
    ('Total AHI: 15.8', '15.8'),
    ('AHI: 11.1', '11.1'),
    ('AHI 12.3', '12.3'),
    ('AHI - 14.5', '14.5'),
    ('AHI was 13.0', '13.0'),
    ('AHI is 10.5', '10.5'),
    ('AHI (apnea-hypopnea index), events per hour of sleep: 16.2', '16.2'),
    ('Apnea-Hypopnnea Index (AHI): 19.8 per hour', '19.8'),
])
def test_ahi_patterns(sentence, expected_val):
    assert check_pattern(sentence, expected_val, AHI_PAT)
