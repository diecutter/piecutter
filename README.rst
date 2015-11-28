#########
piecutter
#########

`piecutter` is a template rendering framework, written in `Python`_.

Leitmotiv: **render templates against data**, wherever the templates, whatever
the template engine.


*******
Example
*******

Let's import ``piecutter`` and initialize data, as a dictionary:

>>> from __future__ import print_function
>>> import piecutter
>>> data = {u'who': u'world'}

Render text template against data using Python's format:

>>> render = piecutter.PythonFormatEngine()
>>> template = u"Hello {who}!"
>>> output = render(template, data)
>>> print(output)
Hello world!

Templates can be loaded from custom locations. Let's load a file:

>>> load = piecutter.LocalLoader(root=u'../demo/')
>>> with load(u'hello.txt') as template:
...     print(template)
...     output = render(template, data)
Hello {who}!
<BLANKLINE>
>>> print(output)
Hello world!
<BLANKLINE>

Full rendering pipeline is configurable. In the following example, let's render
a template loaded from the internet and send output to standard output stream:

>>> render = piecutter.Cutter(
...     loader=piecutter.HttpLoader(),
...     engine=piecutter.PythonFormatEngine(),
...     writer=piecutter.StreamWriter(),
... )
>>> render(
...     u'https://raw.github.com/diecutter/piecutter/cutter-api-reloaded/demo/hello.txt',
...     data)
Hello world!


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
