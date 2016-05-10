"""Template engine specialized to render filenames."""
from piecutter.engines import Engine


class FilenameEngine(Engine):
    """"""
    def render(self, template, context):
        """Return rendered filename template against context.

        .. warning::

           Only flat string variables are accepted. Other variables are ignored
           silently!

        """
        context.setdefault('piecutter', {})
        context['piecutter']['engine'] = 'filename'
        for key, val in context.iteritems():
            try:
                template = template.replace('+{key}+'.format(key=key), val)
            except TypeError:
                pass
        return template
