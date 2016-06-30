"""Cutters encapsulate template rendering process.

:class:`Cutter` class is the reference implementation.

"""
import contextlib
import json
from pathlib import PurePosixPath
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


class RenderedObject(object):
    def __init__(self):
        #: Name (basename) of the object.
        #:
        #: Example: u"hello.txt".
        self.name = u''

        #: Path of the object, relative to template's root.
        #:
        #: Example: u"simple/hello.txt".
        self.path = u''

        #: Location the object was loaded from, typically an URL.
        #:
        #: May contain template engine's syntax.
        #: Example: u"file://demo/simple/{what}.txt".
        self.location = u''


class RenderedFile(RenderedObject):
    def __init__(self, content):
        super(RenderedFile, self).__init__()
        self.content = content

    def __iter__(self):
        return self.content.__iter__()

    def read(self):
        return ''.join(self)


class RenderedDirectory(RenderedObject):
    def __init__(self, tree=None):
        super(RenderedDirectory, self).__init__()
        self.tree = tree

    def __iter__(self):
        return self.tree.__iter__()


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

    def render(self, template, data, path_prefix=None):
        """Return result of template rendered against data."""
        if template.is_file:
            return self.render_file(template, data, path_prefix=path_prefix)
        else:
            return self.render_directory(template,
                                         data,
                                         path_prefix=path_prefix)

    def render_file(self, template, data, path_prefix=None):
        name = template.name
        if name:
            name = self.engine.render(
                piecutter.TextTemplate(template.name),
                data).read()
        path = name
        if path_prefix:
            path = PurePosixPath(path_prefix) / PurePosixPath(path)
        result = RenderedFile(content=self.engine.render(template, data))
        setattr(result, 'location', template.location)
        setattr(result, 'name', name)
        setattr(result, 'path', path)
        return result

    def render_directory(self, template, data, path_prefix=None):
        name = template.name
        if name:
            name = self.engine.render(
                piecutter.TextTemplate(name),
                data).read()
        path = name
        if path_prefix:
            path = unicode(PurePosixPath(path_prefix) / PurePosixPath(path))
        tree = self.render_directory_items(template, data, path_prefix=path)
        result = RenderedDirectory(tree=tree)
        setattr(result, 'location', template.location)
        setattr(result, 'name', name)
        setattr(result, 'path', path)
        return result

    def render_directory_items(self, template, data, path_prefix=None):
        """Generate file and Directory object for each item in directory."""
        try:
            tree = self.dynamic_tree(template, data)
        except (AttributeError, piecutter.TemplateNotFound):
            tree = self.static_tree(template, data)
        for location, filename, data_overrides in tree:
            local_data = data.copy()
            local_data.update(data_overrides)
            location = relative_to(template.location, location)
            with self.open(location) as sub_template:
                result = self.render(sub_template,
                                     local_data,
                                     path_prefix=path_prefix)
            rendered_name = self.engine.render(
                piecutter.TextTemplate(filename),
                local_data).read()  # May differ from template's original name.
            path = rendered_name
            if path_prefix:
                path = unicode(
                    PurePosixPath(path_prefix) / PurePosixPath(path))
            setattr(result, 'name', rendered_name)
            setattr(result, 'path', path)
            yield result

    def static_tree(self, template, data):
        """Return static list of files in template directory.

        The result is a list of ``(location, filename, data)``.

        """
        tree = []
        for location in self.loader.tree(template.location):
            name = location[len(template.location):].lstrip('/')  # HACK!
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
