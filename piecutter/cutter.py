"""Cutters encapsulate template rendering process.

:class:`Cutter` class is the reference implementation.

"""
import contextlib
import json

import piecutter


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
        #: Loader.
        self.loader = loader
        if self.loader is None:
            self.loader = piecutter.ProxyLoader()

        #: Engine.
        self.engine = engine
        if self.engine is None:
            self.engine = piecutter.PythonFormatEngine()

        #: Writer.
        self.writer = writer
        if self.writer is None:
            self.writer = piecutter.TransparentWriter()

    @contextlib.contextmanager
    def open(self, location):
        """Return template resource."""
        with self.loader.open(location) as template:
            template.loader = self.loader
            template.location = location
            yield template

    def render(self, template, data):
        """Return result of template rendered against data."""
        if template.is_file:
            return self.render_file(template, data)
        else:
            return self.render_directory(template, data)

    def render_file(self, template, data):
        return self.engine.render(template, data)

    def render_directory(self, template, data):
        try:
            tree_location = self.loader.tree_template(template.location)
            with self.open(tree_location) as tree_template:
                encoded_tree = self.render_file(tree_template, data)
            tree = json.load(encoded_tree)
        except (AttributeError, piecutter.TemplateNotFound):
            tree = self.loader.tree(template.location)
        for location, overrides, name in tree:
            rendered_name = self.render_file(name, data).read()
            local_data = data
            local_data.update(overrides)
            result = self(location, local_data)
            setattr(result, 'name', rendered_name)
            yield result

    def write(self, content):
        """Process ``content``."""
        return self.writer.write(content)

    def __call__(self, location, data):
        """Process template at ``location`` with ``data``.

        Executes the full process on a template: load, render, write.

        """
        with self.open(location) as template:
            output = self.render(template, data)
            return self.write(output)
