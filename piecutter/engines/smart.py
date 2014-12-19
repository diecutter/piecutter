"""Multi-purpose engine."""
from piecutter.engines import Engine


class SmartEngine(Engine):
    """Multi-purpose engine which delegates task to the best match."""
    def __init__(self, engines=None):
        super(SmartEngine, self).__init__()

        #: Iterable of engines (instances) candidates. Their order matters.
        self.engines = engines
        if self.engines is None:
            self.engines = []

    def render(self, template, context):
        """Render template against context, with best match engine.

        Uses :attr:`engines`' :meth:`piecutter.engines.Engine.match` method.

        """
        matches = []
        for engine in self.engines:
            matcher = engine.match  # Engines should implement ``match()``
            match = matcher(template, context)
            matches.append((match, engine))
            if match >= 1:
                break
        if matches:
            matches.sort(reverse=True)
            best_match = matches[0][1]
            return best_match.render(template, context)
