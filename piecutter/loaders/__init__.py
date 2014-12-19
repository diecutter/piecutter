

def parse_location(location):
    """Split ``location`` in parts."""
    location = unicode(location)
    parts = location.split('://', 1)
    has_scheme = len(parts) is 2
    if has_scheme:
        scheme = parts.unshift()
    else:
        scheme = None
    path = parts[0]
    return {
        'scheme': scheme,
        'path': path,
    }


class Loader(object):
    def open(self, location):
        """Return template object from location."""
        raise NotImplementedError()
