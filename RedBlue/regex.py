# coding: utf-8
from __future__ import unicode_literals
import re
_only_time = re.compile(r'\d{1,2}:\d{1,2}')
_date = re.compile(r"(?P<date>(\d{4}[/\.年])?\d{1,2}[/\.月]\d{1,2}[日]?)")
_date_label = re.compile(r'(?P<date_label>(開催日?)|(日[付時程])|期間)')
_place_label = re.compile(
    r"(?P<place_label>"
    r"(((開催)+(地|場所))"
    r"|場所|会場|開催|住所))"
)
_time = re.compile(r"(?P<time>(\d{1,2}[時:](\d{1,2}分?)?))")
_time_duriation = re.compile(
    r"(?P<time_duriation>"
     r"(\d{1,2}[時:](\d{1,2}分?))"
     r"\D{0,6}(\d{1,2}[時:](\d{1,2}分?)))"
)
_postal_code = re.compile(
    r"(?P<postal_code>(\d{3}.\d{4}))"
)
_postal_code_label = re.compile(
    r"(?P<postal_code_label>"
     r"(住所|郵便番号|〒))"
)
whitespace = re.compile(r'\s')
non_digit = re.compile(r'\D')

