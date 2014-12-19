"""Writers post-process the output of template rendering."""
from __future__ import print_function
import sys


class Writer(object):
    """Base class for writers."""
    def write(self, content):
        """Post-process template-rendering result."""
        raise NotImplementedError('Subclasses must implement "write()" method')

    def __call__(self, *args, **kwargs):
        """Proxy to :meth:`write`."""
        return self.write(*args, **kwargs)


class StreamWriter(Writer):
    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stdout
        self.stream = stream

    def write(self, content):
        self.stream.write(content)


class PrintWriter(Writer):
    def write(self, content):
        print(content)
