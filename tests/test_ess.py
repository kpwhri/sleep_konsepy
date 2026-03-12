import pytest

from sleep_konsepy.concepts.ess import ESS_PAT
from tests.utils import check_pattern


@pytest.mark.parametrize('sentence, expected_val', [
    ('Epworth Sleepiness Scale: 12 out of 24', '12'),
    ('Epworth Sleepiness Scale: 10 / 24', '10'),
    ('EPWORTH SLEEPINESS SCALE: 8', '8'),
    ('Epworth Sleepiness Scale: 14', '14'),
    ('ESS of 11/24', '11'),
    ('Epworth Score: 9', '9'),
    ('Epworth: 15/24', '15'),
    ('Epworth: 13', '13'),
    ('EPWORTH: 7/24', '7'),
    ('EPWORTH 6/24', '6'),
    ('Epworth Sleepiness Score (ESS): 18 out of a possible 24', '18'),
    ('Epworth 11', '11'),
    ('Epworth Sleepiness Scale (0-24): 12', '12'),
    ('Epworth Sleepiness Scale was 10', '10'),
    ('Epworth Sleepiness Score of 9/24', '9'),
    ('Epworth Sleepiness Score is 11', '11'),
    ('Epworth is 14 out of 24', '14'),
    ('Epworth sleep score : 15/24', '15'),
    ('Epworth sleepiness scale was 10/24', '10'),
    ('Epworth sleepiness score 12', '12'),
    ('Epworth sleepiness score 13/24', '13'),
    ('Epworth sleepiness score is only 5', '5'),
    ('Epworth score 14/24', '14'),
    ('Epworth sleepiness scale = 11', '11'),
    ('Epworth score is estimated at 12/24', '12'),
    ('Epworth scale only 8', '8'),
    ('Epworth score is 13/24', '13'),
    ('Epworth score= 14/24', '14'),
    ('Epworth Sleepiness Score: 10/24', '10'),
    ('Epworth sleepiness scale is 15/24', '15'),
    ('Epworth Sleepiness Score today is 12 out of 24', '12'),
    ('Epworth sleepiness scale quite high, 18 out of 24', '18'),
    ('Epworth Sleepiness Score today is 11/24', '11'),
    ('Epworth sleepiness scale 10/24', '10'),
    ('Epworth sleepiness score is 14/24', '14'),
    ('Epworth sleep score: 13', '13'),
    ('Epworth sleepiness score of 12', '12'),
    ('Epworth sleepiness scale last visit was 9/24', '9'),
    ('Epworth was 11/24', '11'),
    ('Epworth Sleepiness Score today is 14/24.', '14'),
    ('Epworth sleepiness score is 12', '12'),
])
def test_ess_patterns(sentence, expected_val):
    assert check_pattern(sentence, expected_val, ESS_PAT)
