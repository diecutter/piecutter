#########
piecutter
#########

`piecutter` is a template rendering framework, written in `Python`_.

Leitmotiv: **render templates against data**, wherever the templates, whatever
the template engine.


************
Key features
************

**Simple API**: ``render(template, data)``.

**Renders files** (single templates) **and directories** (collections of
templates).

**Multiple template engines**: `Python's format()`_, `Jinja2`_ and `Django`_...
Additional engines such as `Cheetah`_ or non-Python template engines such as
Ruby's `ERB`_ could be supported.

**Extensible template loading**: text, bytes, file-like objects, files on
local filesystem, remote resources over HTTP, remote resources on github.com...
Additional storages could be supported.

**Configurable post-processing**: write to local filesystem, generate an
archive... It's easy to create your own.

**Dynamic directory generation**: generate one template multiple times with
different data, exclude some files depending on context, include external
locations, use several template engines...


********
Examples
********

Hello world!
============

Let's generate the traditional "Hello world!":

>>> import piecutter
>>> template = u'Hello {who}!'  # Simplest template is text. Could be a file.
>>> data = {u'who': u'world'}  # Data can be any dictionary-like object.
>>> render = piecutter.Cutter()  # Default engine uses Python's format().
>>> output = render(template, data)  # Default output is a file-like object.
>>> print(output.read())
Hello world!

With ``piecutter.Cutter``'s default setup, files are rendered as file-like
objects, so that you can iterate over content.

Load files
==========

Let's load and render a template located on local filesystem:

>>> location = u'file://demo/simple/hello.txt'
>>> output = render(location, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

It works the same with a remote template over HTTP:

>>> location = u'https://raw.github.com/diecutter/piecutter/' \
...            u'cutter-api-reloaded/demo/hello.txt'
>>> output = render(location, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

``piecutter.Cutter``'s default loader is a proxy that automatically detects
scheme (``file://`` and ``https://`` in examples above) then dispatches actual
loading to a specialized loader implementation.

Render directories
==================

Given the following directory:

.. code:: text

   demo/simple/
   ├── hello.txt  # Contains "Hello {who}!\n"
   └── {who}.txt  # Contains "Whatever the content.\n"

By default, directories are rendered as generator of file-like objects. So we
can iterate generated items and use their ``name`` attribute and ``read()``
method:

>>> for item in render(u'file://demo/simple/', data):
...     print('Name: {}'.format(item.name))
...     print('Content: {}'.format(item.read()))
Name: hello.txt
Content: Hello world!
<BLANKLINE>
Name: world.txt
Content: Whatever the content.
<BLANKLINE>

Of course, you may want to write output to disk or to an archive. `piecutter`
provides "writers" for that purpose!


**************
Project status
**************

**Yesterday**, `piecutter` was the core of `diecutter`_.

As `diecutter`'s authors, we think `diecutter` has great features related to
templates and file generation. We wanted to share it with a larger audience.
So we just packaged it as a standalone library, and this is `piecutter`.

In early versions, `piecutter` was tied to `diecutter` implementation. The API
reflected `diecutter`'s architecture and concepts, which may sound obscure for
other usage.

**Today**, `piecutter`'s API has been refactored, with simplicity in mind,
independantly from `diecutter`.


*********
Resources
*********

* Documentation: https://piecutter.readthedocs.io
* PyPI page: http://pypi.python.org/pypi/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Changelog: https://piecutter.readthedocs.io/en/latest/about/changelog.html
* Roadmap: https://github.com/diecutter/piecutter/milestones
* Code repository: https://github.com/diecutter/piecutter
* Continuous integration: https://travis-ci.org/diecutter/piecutter


.. _`Python`: https://www.python.org
.. _`diecutter`: http://diecutter.io
.. _`join us`: https://piecutter.readthedocs.io/en/latest/contributing.html
.. _`Python's format()`:
   https://docs.python.org/3/library/string.html#formatstrings
.. _`Jinja2`: http://jinja.pocoo.org/
.. _`Django`: https://www.djangoproject.com
.. _`Cheetah`: http://pythonhosted.org/Cheetah/
.. _`ERB`: http://ruby-doc.org/
