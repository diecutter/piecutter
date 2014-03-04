# -*- coding: utf-8 -*-
"""Tests around piecutter.engines.django."""
import unittest

from piecutter.engines.django import DjangoEngine
from piecutter.exceptions import TemplateError


class DjangoTestCase(unittest.TestCase):
    """Test piecutter.engines.django.DjangoEngine."""
    def test_render_noop(self):
        """DjangoEngine correctly renders ``Hello world!`` template."""
        engine = DjangoEngine()
        rendered = engine.render(u'Hello world!', {})
        self.assertEqual(rendered, u'Hello world!')

    def test_render_simple(self):
        """DjangoEngine correctly renders ``Hello {{ name }}!`` template."""
        engine = DjangoEngine()
        rendered = engine.render(u'Hello {{ name }}!', {'name': 'world'})
        self.assertEqual(rendered, u'Hello world!')

    def test_template_error(self):
        """DjangoEngine raises TemplateError in case of exception."""
        engine = DjangoEngine()
        self.assertRaises(TemplateError,
                          engine.render,
                          u'{% if foo %}Unclosed IF',
                          {})
