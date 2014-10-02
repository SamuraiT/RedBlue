# coding: utf-8
from __future__ import unicode_literals
import sys
import re
from bs4 import BeautifulSoup as BS
from operator import itemgetter, attrgetter
import unicodedata
import sys
from datetime import datetime
from copy import deepcopy
import regex
import MeCab

class Event(object):

    def __init__(self, place, time, duri,
                    date, is_event, confidence, postal_code, soup, num):
        self.place = place
        self.time = time
        self.date = date
        self.duri = duri
        self.is_event = is_event
        self.confidence = confidence
        self.postal_code = postal_code
        self._soup = soup
        self._num = num

    def __repr__(self):
        return '<Event:{n}>'.format(n=self._num)


class Parser(object):

    """
    Event info extractor extracts event data:
    (place, date, time, duriation time,
    judge if this is event or not  and confidence of this)
    give this class a text which you want to examine
    >>> f = open('flask.html')
    >>> events = Parser.read(f)
    >>> e = events[0]
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
    _soup = ''
    is_calculated = False


    def obtain_event_info_from_text(self, text=None):
        if not text:text = self.text
        self.datels = self.span_label(regex._date_label, text)
        self.dates = self.span_label_datetime(regex._date, text)
        self.date_dis = self.distance(self.datels, self.dates)
        self.times = self.span_label(regex._time, text)
        self.time_dis = self.distance(self.datels, self.times)
        self.duris = self.span_label_time(regex._time_duriation, text)
        self.duri_dis = self.distance(self.datels, self.duris)
        self.placels = self.span_label(regex._place_label, text)
        self.places = self.get_place(text)
        self.place_dis = self.distance(self.placels, self.places)
        self.postal_codes = self.span_label(regex._postal_code, text)
        self.postal_codels = self.span_label(regex._postal_code_label, text)
        self.postal_code_dis = self.distance(
                self.postal_codels,
                self.postal_codes)
        self.is_calculated = True

    @classmethod
    def read(cls, fobj):
        parser = Parser()
        parser.read_text(fobj)
        return [Event(
                    place = parser.place,
                    time = parser.time,
                    date = parser.date,
                    duri = parser.duri,
                    postal_code = parser.postal_code,
                    is_event = parser.is_event,
                    confidence = parser.confidence,
                    soup = parser._soup,
                    num = 0
                    )
                ]


    def num_of_events(self):
        #TODO must support mulit events
        return 1


    def read_text(self, text):
        soup = BS(text)
        self._soup = soup
        [s.extract() for s in soup('script')]
        text = regex.whitespace.sub('', soup.text)
        text = unicodedata.normalize('NFKC', text)
        self.obtain_event_info_from_text(text=text)
        return text

    
    def span_label_datetime(self, regx, text):
        return [dict(label=self.str2datetime(m.group()),span=m.span())
                    for m in regx.finditer(text)]

    
    def span_label_time(self, regx, text):
        return [dict(label=regex._only_time.findall(m.group()),span=m.span())
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
        if sys.version > '3':
            decode = lambda txt: txt
            encode = lambda txt: txt
        else:
            decode = lambda txt: txt.decode('utf-8')
            encode = lambda txt: txt.encode('utf-8')
        status = 0
        place = 0
        t = [[]]
        utext = text
        text = encode(text) #create variable for mecab memory problem
        mecab = MeCab.Tagger(encode("-Ochasen"))
        node = mecab.parseToNode(text)
        while node:
            f = node.feature
            if u'地域' in decode(f):
                status = 1
                t[place].append(decode(node.surface))
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
            place.extend(self.span_label(re.compile(encode(each)), text))
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
        _ = lambda code: regex.non_digit.sub('', code)
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
            date = datetime.strptime(dtstr, r"%m月%d日")
            date = datetime(datetime.now().year, date.month, date.day)
            return date
        except ValueError:
            pass
        try:
            date = datetime.strptime(dtstr, r"%Y年%m月%d日")
            return date
        except ValueError:
            pass
        try:
            date = datetime.strptime(dtstr, r"%Y/%m/%d")
            return date
        except ValueError:
            pass
        try:
            date = datetime.strptime(dtstr, r"%m/%d")
            date =  datetime(datetime.now().year, date.month, date.day)
            return date
        except ValueError:
            pass
        return date

events = Parser.read(open('flask.html'))
e = events[0]
