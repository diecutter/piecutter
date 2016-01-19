#########
piecutter
#########

`piecutter` is a template rendering framework, written in `Python`_.

Leitmotiv: **render templates against data**, wherever the templates, whatever
the template engine.


********
Abstract
********

`piecutter` implements the ``render(template, data)`` pattern:

* ``template`` can be text, file, directory, ... It can live in memory, on
  local filesystem, on remote locations, ... And whatever the template
  language;

* ``data`` is any dictionary-like (i.e. mapping) object;

* ``render`` encapsulates loading template, rendering template against data,
  and post-processing output. Each part of the pipeline is configurable.

`piecutter`'s challenge is to provide dead-simple defaults to cover most
use-cases, and configurable objects to cover specific situations.


*******
Example
*******

Let's import ``piecutter`` and initialize data, as a dictionary:

>>> from __future__ import print_function
>>> import piecutter
>>> data = {u'who': u'world'}

Let's render text template:

>>> template = u'Hello {who}!'
>>> render = piecutter.Cutter()
>>> output = render(template, data)
>>> print(output.read())
Hello world!

By default, ``piecutter.Cutter`` uses Python format. But it also supports other
template engines, such as Jinja2:

>>> template = u'Hello {{ who }}!'
>>> render = piecutter.Cutter(engine=piecutter.Jinja2Engine())
>>> output = render(template, data)
>>> print(output.read())
Hello world!

`piecutter` has builtin support for the following template engines: Python
format, Jinja2, Django. And feel free to add support for additional ones:
`piecutter` has been developed with extensibility in mind!

There is also a special engine that guesses the best engine to use depending on
the template's name, content and context.

Templates can be loaded from various locations. The examples above show text
templates. Here is another example using a file object:

>>> render.engine = piecutter.PythonFormatEngine()  # Restore initial engine.
>>> with open('demo/hello.txt') as template:
...     output = render(template, data)
...     print(output.read())
Hello world!
<BLANKLINE>

Here is another example using a local file:

>>> template = u'file://demo/hello.txt'
>>> output = render(template, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

And another example using a remote template over HTTP:

>>> template = u'https://raw.github.com/diecutter/piecutter/' \
...            u'cutter-api-reloaded/demo/hello.txt'
>>> output = render(template, data)
>>> print(output.read())
Hello world!
<BLANKLINE>

Full rendering pipeline is configurable through loaders, engines and writers.
The ``piecutter.Cutter`` encapsulates such components:

>>> render  # doctest: +ELLIPSIS
<piecutter.cutter.Cutter object at 0x...>
>>> render.loader  # doctest: +ELLIPSIS
<piecutter.loaders.proxy.ProxyLoader object at 0x...>
>>> render.engine  # doctest: +ELLIPSIS
<piecutter.engines.pythonformat.PythonFormatEngine object at 0x...>
>>> render.writer  # doctest: +ELLIPSIS
<piecutter.writers.TransparentWriter object at 0x...>

With ``piecutter.Cutter``'s default setup, files are rendered as file-like
objects, so that you can iterate over content.

Collections of templates, a.ka. directories, are also supported. By default,
they are rendered as generator of multiple file-like objects. As an example,
let's inspect the "demo/" directory we are about to render:

>>> import os
>>> print(sorted(os.listdir('demo/')))
['hello.txt', '{who}.txt']

When we render the directory, we get a generator:

>>> output = render(u'file://demo/', data)
>>> output  # doctest: +ELLIPSIS
<generator object ... at 0x...>

Each file is rendered as a file-like object.
The first one is our previous "hello.txt" example:

>>> item = output.next()
>>> print(item.name)
hello.txt
>>> print(item.read())
Hello world!
<BLANKLINE>

The second one has a dynamic name:

>>> item = output.next()
>>> print(item.name)
world.txt
>>> print(item.read())
Whatever the content.
<BLANKLINE>






************
Key features
************

* Simple API: render templates against context.

* Support multiple template engines: `Jinja2`_ and `Django`_ for now. Later:
  `Cheetah`_ and even non-Python template engines such as Ruby's `ERB`_.

* Render files and directories.

* Load templates from almost everywhere: local filesystem and github.com for
  now. Later: Django storages...

* Do what you want with generated content: write to local filesystem, generate
  an archive...


**************
Project status
**************

`piecutter` is under active development.

**Yesterday**, `piecutter` was the core of `diecutter`_.

As `diecutter`'s authors, we think `diecutter` has great features related to
templates and file generation. We wanted to share it with a larger audience.
So we just packaged it as a standalone library.
And we are planning to make it better as soon as possible.
`Join us`_ if you like the features ;)

Here are some of our motivations:

* third-party projects can use `piecutter`. They do not have to depend on
  `diecutter`, which embeds some specific code related to its web service.

* as a standalone library, `piecutter` should be easier to maintain and
  improve.

* `piecutter` is more open than `diecutter`. It can have a larger community.
  It also may converge with similar tools.

**Today**, `piecutter` is tied to `diecutter` implementation. The API
reflects `diecutter`'s architecture and concepts, which may sound obscure for
other usage.

**Tomorrow**, we are planning to improve `piecutter`. As an example, we think
the API should be refactored, with simplicity in mind.


*********
Resources
*********

* Documentation: https://piecutter.readthedocs.org
* PyPI page: https://pypi.python.org/pypi/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Changelog: https://piecutter.readthedocs.org/en/latest/about/changelog.html
* Roadmap: https://github.com/diecutter/piecutter/milestones
* Code repository: https://github.com/diecutter/piecutter
* Continuous integration: https://travis-ci.org/diecutter/piecutter


.. _`Python`: https://www.python.org
.. _`diecutter`: http://diecutter.io
.. _`join us`: https://piecutter.readthedocs.org/en/latest/contributing.html
.. _`Jinja2`: http://jinja.pocoo.org/
.. _`Django`: https://www.djangoproject.com
.. _`Cheetah`: http://pythonhosted.org/Cheetah/
.. _`ERB`: http://ruby-doc.org/
