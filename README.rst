#########
piecutter
#########

`piecutter` is a template rendering framework, written in `Python`_.

Leitmotiv: **render templates against context**, wherever the templates,
whatever the template engine.


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


*******
Example
*******

Here is a simple demo of `piecutter`'s API:

.. code:: pycon

   >>> import piecutter
   >>> cutter = piecutter.Cutter(engine=piecutter.PythonFormatEngine())
   >>> print(cutter.render("Hello {who}!", {'who': 'world'}))
   Hello world!

Here is another setup, where several template engines are registered:

.. code:: pycon

   >>> cutter = piecutter.Cutter(
   ...     engine=piecutter.GuessEngine(
   ...         engines=[
   ...             piecutter.Jinja2Engine(),
   ...             piecutter.DjangoEngine(),
   ...             piecutter.PythonFormatEngine(),
   ...         ],
   ...     )
   ... )

Then we can use the cutter to render various templates:

.. code:: pycon

   >>> cutter.render("{# Jinja2 #}Hello {{ who }}!", {'who': 'world'})
   'Hello world!'
   >>> cutter.render("{# Django #}Hello {{ who }}!", {'who': 'world'})
   'Hello world!'
   >>> cutter.render("Hello {who}!", {'who': 'world'})
   'Hello world!'


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


*********
Resources
*********

* Documentation: https://piecutter.readthedocs.io
* PyPI page: http://pypi.python.org/pypi/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Changelog: https://piecutter.readthedocs.io/en/latest/about/changelog.html
* Roadmap: https://github.com/diecutter/piecutter/issues/milestones
* Code repository: https://github.com/diecutter/piecutter
* Continuous integration: https://travis-ci.org/diecutter/piecutter


.. _`Python`: https://python.org
.. _`diecutter`: http://diecutter.io
.. _`join us`: https://piecutter.readthedocs.io/en/latest/contributing.html
.. _`Jinja2`: http://jinja.pocoo.org/
.. _`Django`: https://djangoproject.com
.. _`Cheetah`: http://pythonhosted.org/Cheetah/
.. _`ERB`: http://ruby-doc.org/
