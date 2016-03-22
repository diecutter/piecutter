# -*- coding: utf-8 -*-
"""Django template engine."""
from __future__ import absolute_import  # Remove ambiguity of ``import django``
from io import StringIO
import re

import django
from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError

from piecutter.engines import Engine
from piecutter.exceptions import TemplateError


settings.configure(LOGGING_CONFIG={})
django.setup()


class DjangoEngine(Engine):
    """Django template engine."""
    def render(self, template, context):
        """Return the rendered template against context."""
        context.setdefault('piecutter', {})
        context['piecutter']['engine'] = 'django'
        try:
            output = Template(template).render(Context(context))
            output = StringIO(output)
            return output
        except TemplateSyntaxError as e:
            raise TemplateError(e)

    def match(self, template, context):
        """Return a ratio showing whether template looks like using engine.

        >>> from piecutter import TextTemplate
        >>> engine = DjangoEngine()
        >>> engine.match(TextTemplate(''), {})
        0.0
        >>> engine.match(TextTemplate('{# Django #}'), {})
        1.0
        >>> engine.match(TextTemplate('Not shebang {# Django #}'), {})
        0.0
        >>> engine.match(TextTemplate('{{ key }}'), {})
        0.9

        """
        content = template.read()
        # Try to locate a root variable in template.
        if content.startswith('{# Django #}'):
            return 1.0
        if re.search(r'{{ .+ }}', content):
            return 0.9
        return 0.0
