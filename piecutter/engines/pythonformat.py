# -*- coding: utf-8 -*-
"""Template engine using Python's builtin string format."""
import re

from piecutter.engines import Engine


class PythonFormatEngine(Engine):
    """Template engine using Python's builtin string format."""
    def render(self, template, context):
        """Return the rendered template against context.

        >>> engine = PythonFormatEngine()
        >>> engine.render('Hello {who}!', {'who': 'world'})
        'Hello world!'

        """
        return template.format(**context)

    def match(self, template, context):
        """Return a ratio showing whether template looks like using engine.

        >>> engine = PythonFormatEngine()
        >>> engine.match('', {})
        0.0
        >>> engine.match('{key}', {})
        0.9

        """
        # Try to locate a root variable in template.
        if re.search(r'{.+}', template):
            return 0.9
        return 0.0
