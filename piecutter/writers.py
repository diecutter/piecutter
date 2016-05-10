"""Writers post-process the output of template rendering."""
from __future__ import print_function
import os
import sys


class Writer(object):
    """Writers post-process generated content.

    Subclasses MUST implement :meth:`write`.

    """
    def write(self, content):
        """Post-process template-rendering result."""
        raise NotImplementedError('Subclasses must implement "write()" method')

    def __call__(self, *args, **kwargs):
        """Proxy to :meth:`write`."""
        return self.write(*args, **kwargs)


class TransparentWriter(Writer):
    """A writer that just returns input as output."""
    def write(self, content):
        return content


class StreamWriter(Writer):
    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stdout
        self.stream = stream

    def write(self, content):
        self.stream.writelines(content)


class PrintWriter(Writer):
    def write(self, content):
        print(content.read())


class FileWriter(Writer):
    def __init__(self, target=None):
        self.target = target
        if self.target is None:
            self.target = os.getcwd()

    def write(self, content):
        written = []
        if hasattr(content, 'name'):
            filename = os.path.join(self.target, content.name)
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(filename, 'wb') as outfile:
                outfile.write(content.read())
                written.append(filename)
        else:
            for item in content:
                written.extend(self.write(item))
        return written
