############
Contributing
############

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

This document provides guidelines for people who want to contribute to the
project.


*********
Resources
*********

* Code repository: https://github.com/diecutter/piecutter
* Bugtracker: https://github.com/diecutter/piecutter/issues
* Continuous integration: https://travis-ci.org/diecutter/piecutter


*******************************************
Create tickets: bugs, features, feedback...
*******************************************

The best way to send feedback is to file an issue in the `bugtracker`_.

Please use the `bugtracker`_ **before** starting some work:

* check if the bug or feature request has already been filed. It may have been
  answered too!

* else create a new ticket.

* if you plan to contribute, tell us, so that we are given an opportunity to
  give feedback as soon as possible.

* in your commit messages, reference the ticket with some ``refs #TICKET-ID``
  syntax.


******************
Use topic branches
******************

* Work in branches.

* Prefix your branch with the ticket ID corresponding to the issue. As an
  example, if you are working on ticket #23 which is about contribute
  documentation, name your branch like ``23-contribute-doc``.

* If you work in a development branch and want to refresh it with changes from
  master, please `rebase`_ or `merge-based rebase`_, i.e. do not merge master.


***********
Fork, clone
***********

Clone `piecutter` repository (adapt to use your own fork):

.. code:: sh

   git clone git@github.com:<your-github-username-here>/piecutter.git
   cd piecutter/


*******************************
Setup a development environment
*******************************

System requirements:

* `Python`_ version 2.7 (in a `virtualenv`_ if you like).
* make and wget to use the provided `Makefile`.

Execute:

.. code:: sh

   make develop


*************
Usual actions
*************

The `Makefile` is the reference card for usual actions in development
environment:

* Install development toolkit with `pip`_: ``make develop``.

* Run tests with `tox`_: ``make test``.

* Build documentation: ``make documentation``. It builds `Sphinx`_
  documentation in `var/docs/html/index.html`.

* Release `piecutter` project with `zest.releaser`_: ``make release``.

* Cleanup local repository: ``make clean``, ``make distclean`` and
  ``make maintainer-clean``.


.. rubric:: Notes & references

.. target-notes::

.. _`bugtracker`: https://github.com/diecutter/piecutter/issues
.. _`rebase`: http://git-scm.com/book/en/Git-Branching-Rebasing
.. _`merge-based rebase`: http://tech.novapost.fr/psycho-rebasing-en.html
.. _`Python`: http://python.org
.. _`virtualenv`: http://virtualenv.org
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`tox`: https://pypi.python.org/pypi/tox/
.. _`Sphinx`: https://pypi.python.org/pypi/Sphinx/
.. _`zest.releaser`: https://pypi.python.org/pypi/zest.releaser/
