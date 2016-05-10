# -*- coding: utf-8 -*-
"""Tests around :mod:`piecutter.cutter`."""
import unittest

import piecutter


class CutterTestCase(unittest.TestCase):
    def test_render_pythonformat(self):
        render = piecutter.Cutter(
            engine=piecutter.PythonFormatEngine(),
        )
        self.assertEqual(
            render("Hello {who}!", {'who': 'world'}).read(),
            'Hello world!')

    def test_render_jinja2(self):
        render = piecutter.Cutter(
            engine=piecutter.Jinja2Engine(),
        )
        self.assertEqual(
            render("Hello {{ who }}!", {'who': 'world'}).read(),
            'Hello world!')

    def test_render_django(self):
        render = piecutter.Cutter(
            engine=piecutter.DjangoEngine(),
        )
        self.assertEqual(
            render("Hello {{ who }}!", {'who': 'world'}).read(),
            'Hello world!')

    def test_render_multiple(self):
        render = piecutter.Cutter(
            engine=piecutter.ProxyEngine(),
        )
        self.assertEqual(
            render("{# Jinja2 #}\nHello {{ who }}!", {'who': 'world'}).read(),
            '\nHello world!')
        self.assertEqual(
            render("{# Django #}\nHello {{ who }}!", {'who': 'world'}).read(),
            '\nHello world!')
        self.assertEqual(
            render("Hello {who}!", {'who': 'world'}).read(),
            'Hello world!')
