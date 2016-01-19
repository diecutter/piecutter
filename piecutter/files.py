from io import BytesIO

from django.core.files.base import File
from django.utils.encoding import force_bytes


class VirtualFile(File):
    """Wrapper for files that live in memory."""
    def __init__(self, file=None, name=u'', url='', size=None):
        """Constructor.

        file:
          File object. Typically an io.StringIO.

        name:
          File basename.

        url:
          File URL.

        """
        super(VirtualFile, self).__init__(file, name)
        self.url = url
        if size is not None:
            self._size = size

    def _get_size(self):
        try:
            return self._size
        except AttributeError:
            try:
                self._size = self.file.size
            except AttributeError:
                self._size = len(self.file.getvalue())
        return self._size

    def _set_size(self, value):
        return super(VirtualFile, self)._set_size(value)

    size = property(_get_size, _set_size)

    def __iter__(self):
        """Same as ``File.__iter__()`` but using ``force_bytes()``.

        See https://code.djangoproject.com/ticket/21321

        """
        # Iterate over this file-like object by newlines
        buffer_ = None
        for chunk in self.chunks():
            chunk_buffer = BytesIO(force_bytes(chunk))

            for line in chunk_buffer:
                if buffer_:
                    line = buffer_ + line
                    buffer_ = None

                # If this is the end of a line, yield
                # otherwise, wait for the next round
                if line[-1] in ('\n', '\r'):
                    yield line
                else:
                    buffer_ = line

        if buffer_ is not None:
            yield buffer_
