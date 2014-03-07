# -*- coding: utf-8 -*-


class TemplateNotFound(Exception):
    """A template resource (file or directory) was not found."""


class TemplateError(Exception):
    """A template failed to be rendered."""
    pass
