# -*- coding: utf-8 -*-
"""Piecutter: template rendering framework."""
import pkg_resources

# API shortcuts.
from piecutter.api import *  # NoQA


#: Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version
