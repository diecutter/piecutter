"""Multi-purpose engine."""
from piecutter.engines import Engine
from piecutter.engines.django import DjangoEngine  # NoQA
from piecutter.engines.jinja import Jinja2Engine  # NoQA
from piecutter.engines.pythonformat import PythonFormatEngine  # NoQA


class ProxyEngine(Engine):
    """Multi-purpose engine which delegates task to the best match."""
    def __init__(self, engines=None):
        super(ProxyEngine, self).__init__()

        #: Dictionary of engines (instances) candidates.
        self.engines = engines
        if self.engines is None:
            self.engines = self.default_engines()

    def default_engines(self):
        """Return list of default engines."""
        return {
            'django': DjangoEngine(),
            'jinja2': Jinja2Engine(),
            'pythonformat': PythonFormatEngine(),
        }

    def route(self, template, context):
        """Return name of best engine found for template and context."""
        matches = []
        route = None
        for key, engine in self.engines.items():
            matcher = engine.match  # Engines should implement ``match()``
            match = matcher(template, context)
            matches.append((match, key))
            if match >= 1:
                return key
        if matches:
            matches.sort(reverse=True)
            route = matches[0][1]
        return route

    def render(self, template, context):
        """Render template against context, with best match engine.

        Uses :attr:`engines`' :meth:`piecutter.engines.Engine.match` method.

        """
        route = self.route(template, context)
        return self.engines[route].render(template, context)
