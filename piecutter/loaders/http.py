import contextlib

import requests

import piecutter
from piecutter.loaders import Loader


class HttpLoader(Loader):
    @contextlib.contextmanager
    def open(self, location):
        try:
            response = requests.get(location)
        except requests.exceptions.RequestException as exception:
            raise piecutter.TemplateNotFound(exception)
        if response.status_code == 404:
            raise piecutter.TemplateNotFound('Not found')
        template = piecutter.TextTemplate(response.text)
        setattr(template, 'close', lambda: None)
        yield template
