import contextlib

from piecutter.loaders import Loader, parse_location
from piecutter.loaders.http import HttpLoader
from piecutter.loaders.local import LocalLoader
from piecutter import templates


class TextLoader(Loader):
    @contextlib.contextmanager
    def open(self, location):
        yield templates.TextTemplate(location)


class FileObjLoader(Loader):
    @contextlib.contextmanager
    def open(self, location):
        yield templates.FileTemplate(location)


class ProxyLoader(Loader):
    """Proxies loading to the most relevant loader it can find."""
    def __init__(self, routes=None):
        super(ProxyLoader, self).__init__()

        #: Iterable of loaders (instances) candidates.
        self.routes = routes
        if self.routes is None:
            self.routes = self.default_routes()

    def default_routes(self):
        return {
            'text': TextLoader(),
            'fileobj': FileObjLoader(),
            'file': LocalLoader(),
            'http': HttpLoader(),
            'https': HttpLoader(),
        }

    def route(self, location):
        """Return route to location."""
        if isinstance(location, templates.Template):
            return 'template'
        if isinstance(location, basestring):
            parts = parse_location(location[:100])
            return parts['scheme'] if parts['scheme'] else 'text'
        if isinstance(location, file):
            return 'fileobj'
        file_api_methods = ['read']
        is_file = all([hasattr(location, attr) for attr in file_api_methods])
        if is_file:
            return 'fileobj'
        raise ValueError('Cannot guess adequate template loader.')

    def tree_template(self, location):
        route = self.route(location)
        return self.routes[route].tree_template(location)

    def tree(self, location):
        route = self.route(location)
        return self.routes[route].tree(location)

    @contextlib.contextmanager
    def open(self, location):
        route = self.route(location)
        with self.routes[route].open(location) as template:
            yield template
