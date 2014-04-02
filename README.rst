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

.. code:: pycon

   >>> import piecutter
   >>> cutter = Cutter(engine=piecutter.PythonFormatEngine(),
   ...                 loader=piecutter.StringLoader())
   >>> template = cutter.load(u'Hello {who}')
   >>> cutter.render_text(template,
   ...                    context={'who': 'world'})
   u'Hello world'


************
Key features
************

* Simple API: render templates against context.

* Support multiple template engines: Jinja2, Django, Cheetah...

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
