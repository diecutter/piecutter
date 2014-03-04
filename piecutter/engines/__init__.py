# -*- coding: utf-8 -*-
"""Template engines."""


class Engine(object):
    """Base class for template engines.

    Mostly used to document engine API.

    Subclasses must implement :py:meth:`render`:

    >>> from piecutter.engines import Engine
    >>> engine = Engine()
    >>> engine.render('fake-template', {'fake': 1})
    ... # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
      ...
    NotImplementedError: Subclasses of "piecutter.engines.Engine" must
    implement render() method.

    """
    def render(self, template, context):
        """Return the rendered template against context."""
        raise NotImplementedError('Subclasses of "piecutter.engines.Engine" '
                                  'must implement render() method.')
