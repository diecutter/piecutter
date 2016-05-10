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

**Extensible template loading**: local filesystem, HTTP, github.com...
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

>>> import piecutter
>>> template = u'Hello {who}!'
>>> data = {u'who': u'world'}
>>> render = piecutter.Cutter()
>>> output = render(template, data)
>>> print(output.read())
Hello world!

`piecutter` has builtin support for the following template engines:

* `Python's format()`_
* `Jinja2`_
* `Django`_.

Feel free to implement support for additional ones. Non-Python engines could be
supported too!

Load remote file
================

>>> template = u'https://raw.github.com/diecutter/piecutter/' \
...            u'cutter-api-reloaded/demo/hello.txt'
>>> output = render(template, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

`piecutter` can load templates from various locations :

* Python builtins, such as text, bytes, file-like objects, ...
* resources on local filesystem
* remote resources over HTTP
* remote resources on github.com.

Feel free to implement support of additional loaders!

Render directories
==================

With ``piecutter.Cutter``'s default setup, files are rendered as file-like
objects, so that you can iterate over content.

Collections of templates, a.ka. directories, are also supported. By default,
they are rendered as generator of file-like objects.

Given the following directory:

.. code:: text

   demo/
   ├── hello.txt  # Contains "Hello {who}!\n"
   └── {who}.txt  # Contains "Whatever the content.\n"

When we render the directory, we can iterate each generated item and use their
``name`` attribute and ``read()`` method:

>>> for item in render(u'file://demo/', data):
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

<<<<<<< HEAD
* Documentation: https://piecutter.readthedocs.io
* PyPI page: http://pypi.python.org/pypi/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Changelog: https://piecutter.readthedocs.io/en/latest/about/changelog.html
* Roadmap: https://github.com/diecutter/piecutter/issues/milestones
=======
* Documentation: https://piecutter.readthedocs.org
* PyPI page: https://pypi.python.org/pypi/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Changelog: https://piecutter.readthedocs.org/en/latest/about/changelog.html
* Roadmap: https://github.com/diecutter/piecutter/milestones
>>>>>>> cutter-api-reloaded
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
