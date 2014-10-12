"""Cutter class."""


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

    def load(self, location):
        """Return template resource."""
        return self.loader.load(location)

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
        template = self.load(location)
        content = self.render(template, data)
        return self.write(content)
