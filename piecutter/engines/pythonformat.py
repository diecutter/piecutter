# -*- coding: utf-8 -*-
"""Template engine using Python's builtin string format."""
import re

import piecutter
from piecutter.engines import Engine


class PythonFormatEngine(Engine):
    """Template engine using Python's builtin string format."""
    def render(self, template, context):
        context.setdefault('piecutter', {})
        context['piecutter']['engine'] = 'pythonformat'
        template = piecutter.guess_template(template)
        if template.is_file:
            return self.render_file(template, context)
        else:
            return self.render_directory(template, context)

    def render_file(self, template, context):
        """Return the rendered template against context.

        >>> engine = PythonFormatEngine()
        >>> engine.render('Hello {who}!', {'who': 'world'})
        'Hello world!'

        """
        try:
            template.seek(0)
        except (AttributeError, NotImplementedError):
            pass
        return template.read().format(**context)

    def render_directory(self, template, context):
        for sub_template in template.read_tree():
            yield sub_template

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
