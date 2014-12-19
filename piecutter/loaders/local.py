import contextlib
import functools
import os
import pathlib

import piecutter
from piecutter.loaders import Loader, parse_location


class LocalLoader(Loader):
    def __init__(self, root=''):
        #: Limit loading to this directory.
        self.root = self._to_path(root)

    def _to_path(self, path):
        if isinstance(path, basestring):
            return pathlib.Path(path)
        return path

    def read_tree(self, full_path):
        for root, dirs, files in os.walk(str(full_path), topdown=True):
            dirs.sort()
            for file_name in sorted(files):
                full_name = pathlib.Path(os.path.join(root, file_name))
                relative_name = full_name.relative_to(self.root)
                template = piecutter.FileTemplate()
                template.name = str(relative_name)
                yield template

    @contextlib.contextmanager
    def open(self, location):
        scheme, path = parse_location(location)
        path = self._to_path(path)
        full_path = self.root / location
        try:
            full_path.relative_to(self.root)
        except ValueError as exception:
            raise piecutter.TemplateNotFound(
                'Cannot load outside root. Exception was {exception}'
                .format(exception=exception))
        if not full_path.exists():
            raise piecutter.TemplateNotFound(
                'Cannot load {location}'.format(location=location))
        if full_path.is_dir():
            # Return dir template.
            template = piecutter.DirectoryTemplate()
            template.read_tree = functools.partial(self.read_tree, full_path)
            template.close = lambda: None
            yield template
        else:
            # Return file template.
            try:
                file_object = full_path.open('rb')
                template = piecutter.FileTemplate(file_object)
                setattr(template, 'close', file_object.close)
                yield template
            except (IOError, OSError) as exception:
                raise piecutter.TemplateNotFound(exception)
            finally:
                template.close()
