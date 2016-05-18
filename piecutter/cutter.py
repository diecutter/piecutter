"""Cutters encapsulate template rendering process.

:class:`Cutter` class is the reference implementation.

"""
import contextlib
import json
from urlparse import urlparse, urlunparse

import piecutter


def relative_to(directory, location):
    """Return location, relative to directory if not absolute."""
    location_parts = urlparse(location)
    if location_parts.scheme:
        return location
    else:
        directory_parts = urlparse(directory)
        if location_parts.path.startswith('/'):
            path = location_parts.path
        else:
            path = u'/'.join([directory_parts.path.rstrip('/'),
                              location_parts.path])
        return urlunparse([directory_parts.scheme,
                           directory_parts.netloc,
                           path,
                           '',
                           '',
                           ''])


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
            tree = self.dynamic_tree(template, data)
        except (AttributeError, piecutter.TemplateNotFound):
            tree = self.static_tree(template, data)
        for location, filename, data_overrides in tree:
            local_data = data.copy()
            local_data.update(data_overrides)
            rendered_name = self.render_file(filename, local_data).read()
            location = relative_to(template.location, location)
            with self.open(location) as sub_template:
                result = self.render(sub_template, local_data)
            setattr(result, 'location', location)
            setattr(result, 'name', rendered_name)
            yield result

    def static_tree(self, template, data):
        """Return static list of files in template directory.

        The result is a list of ``(location, filename, data)``.

        """
        tree = []
        for location in self.loader.tree(template.location):
            name = location[len(template.location):]
            tree.append([location, name, {}])
        return tree

    def dynamic_tree(self, template, data):
        """Return dynamic template-based list of files in directory.

        The result is a list of ``(location, filename, data)``.

        """
        # Get the tree template's location.
        tree_location = self.loader.tree_template(template.location)
        # Render tree template, without involving writers.
        with self.open(tree_location) as tree_template:
            encoded_tree = self.render_file(tree_template, data).read().strip()
        # Extract raw data from tree template.
        if encoded_tree:
            tree_items = json.loads(encoded_tree)
        else:  # Edge case: empty template.
            tree_items = []
        tree = []
        for item in tree_items:
            tree.append((
                item['template'],
                item.get('filename', item['template']),
                item.get('data', {})
            ))
        return tree

    def write(self, content):
        """Process ``content``."""
        return self.writer(content)

    def __call__(self, location, data):
        """Process template at ``location`` with ``data``.

        Executes the full process on a template: load, render, write.

        """
        with self.open(location) as template:
            output = self.render(template, data)
            return self.write(output)
