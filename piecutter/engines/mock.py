# -*- coding: utf-8 -*-
"""Mock template engine, for use in tests."""
from piecutter.engines import Engine


#: Default value used as :py:attr:`MockEngine.render_result`
default_render_result = u'RENDER template="{template!s}" ' \
                        u'AGAINST context={context!s}'


class MockEngine(Engine):
    """Template engine mock.

    Typical usage:

    >>> from piecutter.engines.mock import MockEngine
    >>> mock_result = u'this is expected result'
    >>> mock = MockEngine(mock_result)
    >>> template = 'arg1'
    >>> context = {'kwarg1': 'kwarg 1', 'kwarg2': 'kwarg 2'}
    >>> mock.render(template, context) == mock_result
    True
    >>> mock.template == template
    True
    >>> mock.context == context
    True

    You can use ``{template}`` and ``{context}`` in mock result, because
    render() uses ``self.render_result.format(template=template,
    context=context)``.
    This feature is used by default:

    >>> mock = MockEngine()
    >>> print mock.render_result
    RENDER template="{template!s}" AGAINST context={context!s}

    If you setup an exception as :py:attr:`fail` attribute,
    then :py:meth:`render` will raise that exception.

    >>> mock = MockEngine(fail=Exception('An error occured'))
    >>> mock.render('', {})  # Doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    Exception: An error occured

    """
    def __init__(self, render_result=default_render_result, fail=None):
        super(MockEngine, self).__init__()

        #: Value to be returned by :py:meth:`render`.
        self.render_result = render_result

        #: Whether to raise a :py:class:`TemplateError` or not.
        #: Also, value used as message in the exception.
        self.fail = fail

        #: Stores ``template`` argument of the last call to :meth:`render`.
        self.template = None

        #: Stores ``context`` argument of the last call to :py:meth:`render`.
        self.context = None

    def render(self, template, context):
        """Return self.render_result + populates template and context.

        If self.fail is not None, then raises a TemplateError(self.fail).

        """
        context.setdefault('piecutter', {})
        context['piecutter']['engine'] = 'mock'
        if self.fail is not None:
            raise self.fail
        self.template = template
        self.context = context
        return self.render_result.format(template=self.template,
                                         context=self.context)
