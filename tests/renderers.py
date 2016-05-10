"""Tests around renderers and engines."""
try:
    from collections.abc import Iterable
except ImportError:  # Python 2.7 fallback
    from collections import Iterable

import piecutter


def test_simple():
    """Renderer accepts template and data and return file object."""
    render = piecutter.PythonFormatEngine()
    template = u'Hello {who}!'
    data = {u'who': u'world'}
    output = render(template, data)
    assert isinstance(output, Iterable)
    assert output.read() == u'Hello world!'
