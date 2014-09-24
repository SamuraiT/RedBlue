The ``example`` module
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
