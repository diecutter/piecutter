# -*- coding: utf-8 -*-
"""Template engine using Python's builtin string format."""
import re
from cStringIO import StringIO

import piecutter
from piecutter.engines import Engine
from piecutter.files import VirtualFile


class PythonFormatEngine(Engine):
    """Template engine using Python's builtin string format."""
    code = u'pythonformat'

    def render(self, template, data):
        data.setdefault('piecutter', {})
        data['piecutter']['engine'] = self.code
        template = piecutter.guess_template(template)
        try:
            template.seek(0)
        except (AttributeError, NotImplementedError):
            pass
        content = template.read()
        output = content.format(**data)
        return VirtualFile(file=StringIO(output))

    def match(self, template, data):
        """Return a ratio showing whether template looks like using engine.

        >>> engine = PythonFormatEngine()
        >>> engine.match('', {})
        0.0
        >>> engine.match('{key}', {})
        0.9

        """
        content = template.read()
        # Try to locate a root variable in template.
        if re.search(r'{.+}', content):
            return 0.9
        return 0.0
