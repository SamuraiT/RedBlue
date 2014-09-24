The ``RedBlue`` module
======================

Using ``RedBlue2``
-------------------

This is the example of RedBlue

    >>> from RedBlue import Event

Now use it:

    >>> e = Event(open('RedBlue2/flask.html'))
    >>> print e.place
    旭川市
    >>> e.date
    datetime.datetime(2013, 11, 10, 0, 0)
    >>> e.duri
    [datetime.datetime(2013, 11, 10, 13, 0), datetime.datetime(2013, 11, 10, 17, 0)]
    >>> e.time
    u'13:00'
    >>> e.postal_code
    u'0700033'
    >>> e.is_event()
    True
    >>> e.confidence()
    87.5
    >>> e.datels == [{'span': (436, 438), 'label': u'\u958b\u50ac'}, \
                    {'span': (514, 516), 'label': u'\u958b\u50ac'}, \
                    {'span': (564, 567), 'label': u'\u958b\u50ac\u65e5'}]
    True
    >>> e.duris == [{'span': (109, 120), 'label': [u'13:00', u'13:05']}, \
                    {'span': (134, 145), 'label': [u'13:05', u'17:00']}, \
                    {'span': (580, 591), 'label': [u'13:00', u'17:00']}]
    True
    >>> e.times ==  [{'span': (109, 114), 'label': u'13:00'}, \
                     {'span': (115, 120), 'label': u'13:05'}, \
                     {'span': (134, 139), 'label': u'13:05'}, \
                     {'span': (140, 145), 'label': u'17:00'}, \
                     {'span': (338, 340), 'label': u'2\u6642'}, \
                     {'span': (580, 585), 'label': u'13:00'}, \
                     {'span': (586, 591), 'label': u'17:00'}]
    True
    >>> e.placels ==  [{'span': (436, 438), 'label': u'\u958b\u50ac'}, \
                       {'span': (474, 476), 'label': u'\u4f1a\u5834'}, \
                       {'span': (514, 518), 'label': u'\u958b\u50ac\u5834\u6240'}, \
                       {'span': (564, 566), 'label': u'\u958b\u50ac'}]
    True

