# -*- coding: utf-8 -*-
"""Template engines."""


class Engine(object):
    """Base class for template engines.

    Mostly used to document engine API.

    Subclasses must implement :meth:`do_render`: and :meth:`match`.

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

    def match(self, template, context):
        """Return probability that template uses engine.

        If a template is not written in engine's syntax, the probability should
        be 0.0.

        If there is no doubt the template has been written for engine, the
        probability should be 1.0. A shebang at the beginning of the template
        may be the safest way to be sure the template has been written for a
        given engine.

        Else, the probability should be strictly between 0.0 and 1.0.

        """
        raise NotImplementedError('Subclasses of "piecutter.engines.Engine" '
                                  'must implement match() method.')

    def __call__(self, template, context):
        """Return rendered ``template`` against ``context`` data."""
        return self.render(template, context)
