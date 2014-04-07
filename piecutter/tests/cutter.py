# -*- coding: utf-8 -*-
"""Tests around :mod:`piecutter.cutter`."""
import unittest

import piecutter


class CutterTestCase(unittest.TestCase):
    def test_render_pythonformat(self):
        cutter = piecutter.Cutter(
            engine=piecutter.PythonFormatEngine(),
        )
        self.assertEqual(
            cutter.render("Hello {who}!", {'who': 'world'}),
            'Hello world!')

    def test_render_jinja2(self):
        cutter = piecutter.Cutter(
            engine=piecutter.Jinja2Engine(),
        )
        self.assertEqual(
            cutter.render("Hello {{ who }}!", {'who': 'world'}),
            'Hello world!')

    def test_render_django(self):
        cutter = piecutter.Cutter(
            engine=piecutter.DjangoEngine(),
        )
        self.assertEqual(
            cutter.render("Hello {{ who }}!", {'who': 'world'}),
            'Hello world!')

    def test_render_multiple(self):
        cutter = piecutter.Cutter(
            engine=piecutter.GuessEngine(
                engines=[
                    piecutter.Jinja2Engine(),
                    piecutter.DjangoEngine(),
                    piecutter.PythonFormatEngine(),
                ],
            )
        )
        self.assertEqual(
            cutter.render("{# Jinja2 #}\nHello {{ who }}!", {'who': 'world'}),
            '\nHello world!')
        self.assertEqual(
            cutter.render("{# Django #}\nHello {{ who }}!", {'who': 'world'}),
            '\nHello world!')
        self.assertEqual(
            cutter.render("Hello {who}!", {'who': 'world'}),
            'Hello world!')
