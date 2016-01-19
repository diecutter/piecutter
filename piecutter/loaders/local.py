import contextlib
import functools
import json
import pathlib

import piecutter
from piecutter.loaders import Loader, parse_location


class LocalLoader(Loader):
    def __init__(self, root=u''):
        #: Limit loading to this directory.
        self.root = self._to_path(root)
        if not self.root.is_dir():
            raise ValueError('Root "{0}" is not a directory'.format(self.root))

    def _to_path(self, path):
        if isinstance(path, basestring):
            return pathlib.Path(path)
        return path

    def tree_template(self, location):
        parts = parse_location(location)
        path = parts['path']
        path = self._to_path(path)
        tree_path = path / pathlib.Path('.directory-tree')
        if parts['scheme']:
            return u'://'.join([parts['scheme'], unicode(tree_path)])
        else:
            return tree_path

    def tree(self, location):
        parts = parse_location(location)
        path = parts['path']
        path = self._to_path(path)
        full_path = self.root / path
        items = []
        file_list = sorted([f for f in full_path.iterdir()])
        for item in file_list:
            relative_path = item.relative_to(full_path)
            item_path = path.joinpath(relative_path)
            if parts['scheme']:
                item_location = u'://'.join([parts['scheme'],
                                             unicode(item_path)])
            else:
                item_location = item_path
            items.append([
                unicode(item_location),
                {},
                unicode(relative_path),
            ])
        return items

    @contextlib.contextmanager
    def open(self, location):
        parts = parse_location(location)
        path = parts['path']
        path = self._to_path(path)
        full_path = self.root / path
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
