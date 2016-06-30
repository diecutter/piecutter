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

**Render files and directories**, a.k.a. single templates and collections of
templates.

**Multiple template engines**: `Python's format()`_, `Jinja2`_ and `Django`_...
Additional engines such as `Cheetah`_ or non-Python template engines such as
Ruby's `ERB`_ could be supported.

**Extensible template loading**: text, bytes, file-like objects, files on
local filesystem, remote resources over HTTP, remote resources on github.com...
Additional storages could be supported.

**Configurable post-processing pipeline**: write to local filesystem, generate
an archive... It's easy to create your own.

**Dynamic directory generation**: generate one template multiple times with
different data, exclude some files depending on context, include templates from
external locations, use several template engines...


********
Examples
********

Hello world!
============

Let's generate the traditional "Hello world!":

>>> import piecutter
>>> template = u'Hello {who}!'  # Text is recognized as a template.
>>> data = {u'who': u'world'}  # Data can be any dictionary-like object.
>>> render = piecutter.Cutter()  # Default engine uses Python's format().
>>> output = render(template, data)  # Default output is a file-like object.
>>> print(output.read())
Hello world!

.. note::

   ``piecutter.Cutter`` provides sane defaults. Then every part of the
   rendering pipeline can be customized in order to fit specific cases.

Load files
==========

Let's load and render a template located on local filesystem:

>>> location = u'file://demo/simple/hello.txt'
>>> output = render(location, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

It works as well with a remote template over HTTP:

>>> location = u'https://raw.github.com/diecutter/piecutter/cutter-api-reloaded/demo/simple/hello.txt'
>>> output = render(location, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

.. note::

   ``piecutter.Cutter``'s default loader detects scheme (``file://`` and
   ``https://`` in examples above) then delegates actual loading to
   specialized loader implementation.

Render directories
==================

Given the following directory:

.. code:: text

   demo/simple/
   ├── hello.txt  # Contains "Hello {who}!\n"
   └── {who}.txt  # Contains "Whatever the content.\n"

By default, directories are rendered as generator of rendered objects. So
can iterate generated items and use their attributes and methods:

>>> for item in render(u'file://demo/simple', data):
...     if isinstance(item, piecutter.RenderedFile):
...         print('File: {}'.format(item.name))
...         print('Path: {}'.format(item.path))
...         print('Content: {}'.format(item.read()))
...     else:  # Is instance of ``piecutter.RenderedDirectory``
...         pass  # We may handle sub-directories recursively here.
File: hello.txt
Path: simple/hello.txt
Content: Hello world!
<BLANKLINE>
File: world.txt
Path: simple/world.txt
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
