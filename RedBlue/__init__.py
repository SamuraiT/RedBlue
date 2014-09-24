import sys
if sys.version > '3':
    from .EventInfoExtractor3 import Event
else:
    from .EventInfoExtractor2 import Event
