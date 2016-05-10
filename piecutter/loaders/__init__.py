

def parse_location(location):
    """Split ``location`` in parts."""
    location = unicode(location)
    parts = location.split('://', 1)
    has_scheme = len(parts) is 2
    if has_scheme:
        scheme = parts.pop(0)
    else:
        scheme = None
    path = parts[0]
    return {
        'scheme': scheme,
        'path': path,
    }


class Loader(object):
    """Loader implements access to locations."""
    def open(self, location):
        """Return template object from location."""
        raise NotImplementedError()

    def is_file(self, location):
        """Return ``True`` if ressource at ``location`` is a file."""
        raise NotImplementedError()

    def is_directory(self, location):
        """Return ``True`` if ressource at ``location`` is a directory."""
        raise NotImplementedError()

    def tree_template(self, location):
        """Return location of dynamic tree template if ``location`` is a dir.

        Raises ``AttributeError`` if ``location`` has no tree template.

        """
        raise NotImplementedError()

    def tree(self, location):
        """Return static list of templates given ``location`` is a dir."""
        raise NotImplementedError()

    def __call__(self, location):
        """Return template object from location."""
        return self.open(location)
