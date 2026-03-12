import enum
import re

from konsepy.rxsearch import search_all_regex_func
from konsepy.rxutils import rx_compile


class AhiCategory(enum.Enum):
    UNKNOWN = -1
    NO = 0
    AHI = 1
    AHI3 = 2
    AHI4 = 3


WS = r'[\s(),=:/-]*'  # no %

pre = r'(?:overall|total)'
value = r'\d+(?:\.\d+)?'
value_capture = rf'(?P<val>{value})'
of = r'(?:of|is|was)'
# events per hour of sleep
events = rf'(?:(?:events{WS})?(?:(?:per|an|/){WS})?(?:(?:hour|hr){WS})(?:of\W*sleep)?)'

ahi = fr'(?:p?ahi|apno?ea{WS}hypopnn?o?ea{WS}index)'
ahi3 = rf'{ahi}{WS}3%'
ahi4 = rf'{ahi}{WS}4%'

value_filler = fr'{WS}(?:(?:{ahi}|{of}|{pre}|{events}){WS})*'

ahi_val = rf'{ahi}{value_filler}{value_capture}'
ahi3_val = rf'{ahi3}{value_filler}{value_capture}'
ahi4_val = rf'{ahi4}{value_filler}{value_capture}'
ahi3_4_val = rf'{ahi3}{value_filler}{value}{WS}(?:{ahi}{WS})?4%{WS}{value_capture}'
ahi4_3_val = rf'{ahi4}{value_filler}{value}{WS}(?:{ahi}{WS})?3%{WS}{value_capture}'

AHI4_PAT = rx_compile(
    rf'(?:'
    rf'{ahi4_val}'
    rf'|{ahi3_4_val}'
    rf')',
    re.IGNORECASE,
)

AHI3_PAT = rx_compile(
    rf'(?:'
    rf'{ahi3_val}'
    rf'|{ahi4_3_val}'
    rf')',
    re.IGNORECASE,
)

AHI_PAT = rx_compile(
    rf'(?:'
    rf'{ahi_val}'
    rf')',
    re.IGNORECASE,
)

REGEXES = [
    (AHI_PAT, AhiCategory.AHI, []),
    (AHI3_PAT, AhiCategory.AHI3, []),
    (AHI4_PAT, AhiCategory.AHI4, []),
]

RUN_REGEXES_FUNC = search_all_regex_func(REGEXES)
