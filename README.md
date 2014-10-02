RedBlue: Event Info Extractor 
===============================
RedBlue is Japanese event infomation extractor. This extracts information such
as `place`, `date`, `datetime`, `duriation time`, etc
and also it justifies weather the given html(text) data is event or not.

Version
-------
You can use both `python 2.x` and `python3.x`.

Why RedBlue
---------
There is no reason. Just sounds a drink I drink often, that's it.

Installtion
-----------

```
pip install git+https://github.com/SamuraiT/RedBlue.git
```

Usage Example (python3)
-------------
See more example: [`example2`](RedBlue/_doctest2.md) for python2

See more example: [`example3`](./example3.md) for python3

    >>> f = open('RedBlue/flask.html')
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


Credit
-----

This program was developed during my time of internship at 
[Shiroyagi Corporation](http://shiroyagi.co.jp/)
