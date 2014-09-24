RedBlue: Event Info Extractor 
===============================
RedBlue is created for extracting event infomation such as 
`place`, `date`, `datetime`, `duriation time`, etc
and also it justifies weather the given text data is event or not.

Why RedBlue
---------
There is no reason. Just sounds a drink I drink often, that's it.

Installtion
-----------

```
pip install git+https://github.com/SamuraiT/RedBlue.git
```

Usage Example
-------------
See [`example.md`](./example.md) for more details.

    >>> from RedBlue import Event
    >>> f = open('RedBlue/flask.html') # open file you want to examine
    >>> e = Event(f)
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


