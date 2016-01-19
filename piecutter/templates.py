"""Templates."""


class Template(object):
    """Base class for template objects."""
    def read(self):
        raise NotImplementedError()

    @property
    def exists(self):
        raise NotImplementedError()

    @property
    def content_type(self):
        """Content-type of the template."""
        raise NotImplementedError()

    @property
    def is_file(self):
        """Return True if resource is a single file."""
        raise NotImplementedError()

    @property
    def is_dir(self):
        """Return True if resource is a collection of files."""
        return not self.is_file

    def __str__(self):
        return str(self.read())

    def __unicode__(self):
        return self.read()

    def seek(self, position):
        raise NotImplementedError()


class DirectoryTemplate(Template):
    """Collection of single templates, as a directory."""
    is_file = False

    def __init__(self, name=None):
        """Constructor."""
        #: Name.
        self.name = name

    @property
    def content_type(self):
        return 'text/directory'

    def read_tree(self):
        """Generate list of paths to contained resources."""

    def read(self):
        """Return computed directory tree as json."""
        data = []
        for template in self.read_tree():
            data.append({
                'template': template.name,
            })
        import json
        return json.dumps(data)

    def __iter__(self):
        """Iterate over template contents."""
        for template in self.read():
            yield template


class SingleTemplate(Template):
    is_file = True


class TextTemplate(SingleTemplate):
    """Template initialized with a text. Lives fully in memory."""
    def __init__(self, template):
        """Constructor."""
        #: Content of the template.
        self.content = template

    def read(self):
        return self.content

    def __str__(self):
        return str(self.read())

    def __unicode__(self):
        return self.read()


class FileTemplate(SingleTemplate):
    """Template initialized with a file-like object."""
    def __init__(self, template=None, name=None, location=None):
        """Constructor."""
        #: File-like object.
        self.file = template

        #: Name.
        self.name = name
        if self.name is None:
            try:
                self.name = self.file.name
            except AttributeError:
                pass

        #: Location on storage (typically filesystem).
        self.location = location

    def open(self, mode='rb'):
        if self.file:
            return self.file.open(mode)
        elif self.location:
            self.file = self.location.open(mode)
            return self.file

    def read(self):
        return self.file.read()

    def seek(self, position):
        return self.file.seek(position)


def guess_template(template):
    if isinstance(template, Template):
        return template
    if isinstance(template, basestring):
        return TextTemplate(template)
    if isinstance(template, file):
        return FileTemplate(template)
    file_api_methods = ['read']
    is_file = all([hasattr(template, attr) for attr in file_api_methods])
    if is_file:
        return FileTemplate(template)
    raise ValueError('Cannot guess template type')


class SmartTemplate(Template):
    """Template initialized with either text, file or template."""
    def __init__(self, template):
        """Constructor."""
        #: Template source, as provided during initialization.
        self.template_source = template

    @property
    def template(self):
        try:
            return self._template_object
        except AttributeError:
            self._template_object = self.guess_template(self.template_source)
            return self._template_object

    def guess_template(self, template):
        return guess_template(template)

    def read(self):
        """Return full template content."""
        return self.template.read()
