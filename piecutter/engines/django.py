# -*- coding: utf-8 -*-
"""Django template engine."""
from __future__ import absolute_import  # Remove ambiguity of ``import django``
import re

from django.conf import settings
from django.template import Template, Context, TemplateSyntaxError

from piecutter.engines import Engine
from piecutter.exceptions import TemplateError

settings.configure()


class DjangoEngine(Engine):
    """Django template engine."""
    def render(self, template, context):
        """Return the rendered template against context."""
        context.setdefault('piecutter', {})
        context['piecutter']['engine'] = 'django'
        try:
            return Template(template).render(Context(context))
        except TemplateSyntaxError as e:
            raise TemplateError(e)

    def match(self, template, context):
        """Return a ratio showing whether template looks like using engine.

        >>> engine = DjangoEngine()
        >>> engine.match('', {})
        0.0
        >>> engine.match('{# Django #}', {})
        1.0
        >>> engine.match('Not shebang {# Django #}', {})
        0.0
        >>> engine.match('{{ key }}', {})
        0.9

        """
        # Try to locate a root variable in template.
        if template.startswith('{# Django #}'):
            return 1.0
        if re.search(r'{{ .+ }}', template):
            return 0.9
        return 0.0
