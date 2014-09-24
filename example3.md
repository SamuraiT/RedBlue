The ``RedBlue`` module
======================

Using ``RedBlue``
-------------------

This is the example of RedBlue

    >>> from RedBlue import Event

Now use it:

    >>> e = Event(open('RedBlue/flask.html'))
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
    >>> e.datels == [{'label': '開催', 'span': (434, 436)}, \
                    {'label': '開催', 'span': (512, 514)}, \
                    {'label': '開催日', 'span': (562, 565)}]
    True
    >>> e.placels == [{'label': '開催', 'span': (434, 436)}, \
                      {'label': '会場', 'span': (472, 474)}, \
                      {'label': '開催場所', 'span': (512, 516)}, \
                      {'label': '開催', 'span': (562, 564)}]
    True
    >>> e.duris == [{'label': ['13:00', '13:05'], 'span': (109, 120)}, \
                    {'label': ['13:05', '17:00'], 'span': (133, 144)},\
                    {'label': ['13:00', '17:00'], 'span': (578, 589)}]
    True
    >>> e.times == [{'label': '13:00', 'span': (109, 114)}, \
                    {'label': '13:05', 'span': (115, 120)}, \
                    {'label': '13:05', 'span': (133, 138)}, \
                    {'label': '17:00', 'span': (139, 144)}, \
                    {'label': '2時', 'span': (336, 338)}, \
                    {'label': '13:00', 'span': (578, 583)}, \
                    {'label': '17:00', 'span': (584, 589)}]
    True

