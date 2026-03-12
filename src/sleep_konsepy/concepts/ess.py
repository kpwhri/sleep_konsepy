import enum
import re

from konsepy.rxsearch import search_all_regex_func
from konsepy.rxutils import rx_compile


class EssCategory(enum.Enum):
    UNKNOWN = -1
    NO = 0
    ESS = 1


WS = r'[\s,=:/-]*'  # no %

ess = r'(?:ess)'
epworth = fr'(?:epworth{WS}(?:sleep(?:iness)?{WS})?(?:(?:score|scale){WS})?)'
epworth_ess = fr'(?:{ess}|{epworth})'

score_range = fr'(?:\(0\s*-\s*24\){WS})'
filler = fr'(?:(?:is|was|of|only|today|high|low|moderate|quite|last\s*visit|estimated|at){WS})*'
value_capture = rf'(?P<val>\d+)'
ess_parens = rf'(?:\(?{ess}\)?{WS})'

ess_score = fr'{epworth_ess}{WS}{ess_parens}?{score_range}?{filler}{value_capture}'

ESS_PAT = rx_compile(
    rf'(?:'
    rf'{ess_score}'
    rf')',
    re.IGNORECASE,
)

REGEXES = [
    (ESS_PAT, EssCategory.ESS, []),
]

RUN_REGEXES_FUNC = search_all_regex_func(REGEXES)
