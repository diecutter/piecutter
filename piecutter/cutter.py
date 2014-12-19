"""Cutters encapsulate template rendering process.

:class:`Cutter` class is the reference implementation.

"""
import contextlib


class Cutter(object):
    """Encapsulate template rendering workflow.

    The idea is that you configure a :class:`Cutter` instance somewhere, then
    you can use it to process (load, render and write) templates.

    A :class:`Cutter` instance manages the relationships between loaders and
    engines. As an example, ``include`` directives interpreted by engine
    during rendering uses the cutter's loaders.

    """
    def __init__(self, loader=None, engine=None, writer=None):
        """Configure template rendering environment."""
        self.loader = loader
        self.engine = engine
        self.writer = writer

    @contextlib.contextmanager
    def open(self, location):
        """Return template resource."""
        with self.loader.open(location) as template:
            yield template

    def render(self, template, data):
        """Return result of template rendered against data."""
        return self.engine.render(template, data)

    def write(self, content):
        """Process ``content``."""
        return self.writer.write(content)

    def __call__(self, location, data):
        """Process template at ``location`` with ``data``.

        Executes the full process on a template: load, render, write.

        """
        with self.open(location) as template:
            return self.write(self.render(template, data))
