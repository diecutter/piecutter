# -*- coding: utf-8 -*-
"""Template engines."""


class Engine(object):
    """Engines render single template against data.

    Subclasses MUST implement :meth:`do_render`: and :meth:`match`.

    """
    def render(self, template, context):
        """Return the rendered template against context."""
        raise NotImplementedError('Subclasses of "piecutter.engines.Engine" '
                                  'must implement render() method.')

    def match(self, template, context):
        """Return probability that template uses engine (experimental).

        If a template is not written in engine's syntax, the probability should
        be 0.0.

        If there is no doubt the template has been written for engine, the
        probability should be 1.0.

        Else, the probability should be strictly between 0.0 and 1.0.

        As an example, here are two ways to be sure template has been written
        for a specific template engine:

        * template's name uses specific file extension
        * there is an explicit shebang at the beginning of the template.

        """
        raise NotImplementedError('Subclasses of "piecutter.engines.Engine" '
                                  'must implement match() method.')

    def __call__(self, template, context):
        """Return rendered ``template`` against ``context`` data."""
        return self.render(template, context)
