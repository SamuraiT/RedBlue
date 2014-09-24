# coding: utf-8
import re
from bs4 import BeautifulSoup as BS
from operator import itemgetter, attrgetter
import unicodedata
import MeCab
import sys
from datetime import datetime
from copy import deepcopy

class Event(object):

    """
    Event info extractor extracts event data:
    (place, date, time, duriation time,
    judge if this is event or not  and confidence of this)
    give this class a text which you want to examine
    >>> e = Event(open('flask.html'))
    >>> e.place
    '旭川市'
    >>> e.date
    datetime.datetime(2013, 11, 10, 0, 0)
    >>> e.duri
    [datetime.datetime(2013, 11, 10, 13, 0), datetime.datetime(2013, 11, 10, 17, 0)]
    >>> e.time
    '13:00'
    >>> e.is_event()
    True
    >>> e.confidence()
    87.5
    >>> e.postal_code
    '0700033'
    """

    def __init__(self, text=None):
        self._only_time = re.compile('\d{1,2}:\d{1,2}')
        self._date = re.compile(u'(?P<date>(\d{4}[/\.年])?\d{1,2}[/\.月]\d{1,2}[日]?)')
        self._date_label = re.compile(u'(?P<date_label>(開催日?)|(日[付時程])|期間)')
        self._place_label = re.compile(u'(?P<place_label>(((開催)+(地|場所))|場所|会場|開催|住所))')
        self._time = re.compile(u'(?P<time>(\d{1,2}[時:](\d{1,2}分?)?))')
        self._time_duriation = re.compile(u'(?P<time_duriation>(\d{1,2}[時:](\d{1,2}分?))\D{0,6}(\d{1,2}[時:](\d{1,2}分?)))')
        self._postal_code = re.compile(u'(?P<postal_code>(\d{3}.\d{4}))')
        self._postal_code_label = re.compile(u'(?P<postal_code_label>(住所|郵便番号|〒))')
        self.whitespace = re.compile('\s')
        self.non_digit = re.compile('\D')
        self.text = self.read_text(text) if text else ''
        self.is_calculated = False

    def obtain_event_info_from_text(self, text=None):
        if not text:text = self.text
        self.datels = self.span_label(self._date_label, text)
        self.dates = self.span_label_datetime(self._date, text)
        self.date_dis = self.distance(self.datels, self.dates)
        self.times = self.span_label(self._time, text)
        self.time_dis = self.distance(self.datels, self.times)
        self.duris = self.span_label_time(self._time_duriation, text)
        self.duri_dis = self.distance(self.datels, self.duris)
        self.placels = self.span_label(self._place_label, text)
        self.places = self.get_place(text)
        self.place_dis = self.distance(self.placels, self.places)
        self.postal_codes = self.span_label(self._postal_code, text)
        self.postal_codels = self.span_label(self._postal_code_label, text)
        self.postal_code_dis = self.distance(
                self.postal_codels,
                self.postal_codes)
        self.is_calculated = True

    def read_text(self, text):
        soup = BS(text)
        [s.extract() for s in soup('script')]
        text = self.whitespace.sub('', soup.text)
        text = unicodedata.normalize('NFKC', text)
        self.obtain_event_info_from_text(text=text)
        return text

    def span_label_datetime(self, regx, text):
        return [dict(label=self.str2datetime(m.group()),span=m.span())
                    for m in regx.finditer(text)]

    def span_label_time(self, regx, text):
        return [dict(label=self._only_time.findall(m.group()),span=m.span())
                    for m in regx.finditer(text)]

    def span_label(self, regx, text):
        return [dict(label=m.group(),span=m.span()) for m in regx.finditer(text)]

    def distance(self, labels, values):
        _dis = []
        for label in labels:
            nearest = float('Inf')
            nearest_lable = ''
            for val in values:
                dis = val['span'][0] - label['span'][1]
                if abs(nearest) > abs(dis):
                    nearest = dis
                    nearest_lable = val['label']
            _dis.append((nearest, dict(label=label['label'],
                value=nearest_lable,dis=nearest)))
        return sorted(_dis, key= lambda x:abs(x[0]))

    def get_place(self, text):
        status = 0
        place = 0
        t = [[]]
        text = text #create variable for mecab memory problem
        mecab = MeCab.Tagger("-Ochasen")
        node = mecab.parseToNode(text)
        while node:
            f = node.feature
            if u'地域' in f:
                status = 1
                t[place].append(node.surface)
            elif status:
                status = 0
                t[place] = ''.join(t[place])
                place += 1
                t.append([])
            node = node.next
        if place:
            del t[place]
        else:
            return t
        t = set(t)
        t = sorted(t, key=len, reverse=True)
        place = []
        for each in t:
            place.extend(self.span_label(re.compile(each), text))
        return place

    def one(self, prop):
        try:
            return prop[0][1]['value']
        except IndexError:
            return None

    @property
    def place(self):
        return self.one(self.place_dis)

    @property
    def date(self):
        return self.one(self.date_dis)

    @property
    def time(self):
        return self.one(self.time_dis)

    @property
    def duri(self):
        t = deepcopy(self.one(self.duri_dis))
        if not t: return t
        if not len(t) == 2:return t
        start_min, start_sec = t[0].split(':')
        end_min, end_sec = t[1].split(':')
        date = self.date
        t[0] = datetime(date.year, date.month, date.day,
                int(start_min), int(start_sec))
        t[1] = datetime(date.year, date.month, date.day,
                int(end_min), int(end_sec))
        return t

    @property
    def postal_code(self):
        _ = lambda code: self.non_digit.sub('', code)
        if self.one(self.postal_code_dis):
            return _(self.one(self.postal_code_dis))
        else:
            return _(self.postal_codes[0].get('label', None))


    def is_event(self, url=None):
        return self.confidence(url) >= 70

    def confidence(self, url=None):
        count = 0
        count += 1.1 if self.place else 0
        count += 1.1 if self.date else 0
        count += 0.9 if self.duri else 0
        count += 0.4 if self.time else 0
        ratio = (count*100) / 4.0
        if not url:
            return ratio
        if 'event' in url or 'events' in url:
            return 100 if ratio+20 > 100 else ratio+20


    def str2datetime(self, dtstr):
        date = dtstr
        try:
            date = datetime.strptime(dtstr, u"%m月%d日")
            date = datetime(datetime.now().year, date.month, date.day)
            return date
        except ValueError:
            pass
        try:
            date = datetime.strptime(dtstr, u"%Y年%m月%d日")
            return date
        except ValueError:
            pass
        try:
            date = datetime.strptime(dtstr, "%Y/%m/%d")
            return date
        except ValueError:
            pass
        try:
            date = datetime.strptime(dtstr, "%m/%d")
            date =  datetime(datetime.now().year, date.month, date.day)
            return date
        except ValueError:
            pass
        return date 


