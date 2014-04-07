#########
piecutter
#########

.. raw:: html

   <a href="http://badge.fury.io/py/piecutter"><img src="https://badge.fury.io/py/piecutter.png"></a>
   <a href="https://travis-ci.org/diecutter/piecutter"><img src="https://travis-ci.org/diecutter/piecutter.png?branch=master"></a>
   <a href="https://crate.io/packages/piecutter?version=latest"><img src="https://pypip.in/d/piecutter/badge.png"></a>

`piecutter` is a templating framework written in Python.


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

* Support multiple template engines with a single API: you render templates
  against context.

* Render files and directories.

* Load templates from almost everywhere: local filesystem, github.com, Django
  storages...

* Do what you want with generated content: write to local filesystem, generate
  an archive...


*********
Resources
*********

* Documentation: https://piecutter.readthedocs.org
* PyPI page: http://pypi.python.org/pypi/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Changelog: https://piecutter.readthedocs.org/en/latest/about/changelog.html
* Roadmap: https://github.com/diecutter/piecutter/issues/milestones
* Code repository: https://github.com/diecutter/piecutter
* Continuous integration: https://travis-ci.org/diecutter/piecutter
