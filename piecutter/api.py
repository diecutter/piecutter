"""API shortcuts.

Everything declared (or imported) in this module is exposed in :mod:`piecutter`
root package, i.e. available when one does ``import piecutter``.

Here are the motivations of such an "api" module:

* as a `piecutter` library user, in order to use `piecutter`, I just do
  ``import piecutter``. It is enough for most use cases. I do not need to
  bother with more `piecutter` internals. I know this API will be maintained,
  documented, and not deprecated/refactored without notice.

* as a `piecutter` library developer, in order to maintain `piecutter` API, I
  focus on things declared in :mod:`piecutter.api`. It is enough. It is
  required. I take care of this API. If there is a change in this API between
  consecutive releases, then I use :class:`DeprecationWarning` and I mention it
  in release notes.

It also means that things not exposed in :mod:`piecutter.api` are not part
of the deprecation policy. They can be moved, changed, removed without notice.

"""
# Exceptions.
from piecutter.exceptions import TemplateNotFound, TemplateError  # NoQA
# Templates.
from piecutter.templates import Template, FileTemplate, TextTemplate  # NoQA
from piecutter.templates import DirectoryTemplate  # NoQA
from piecutter.templates import SmartTemplate, guess_template  # NoQA
# Loaders.
from piecutter.loaders import Loader  # NoQA
from piecutter.loaders.github import GithubLoader  # NoQA
from piecutter.loaders.http import HttpLoader  # NoQA
from piecutter.loaders.local import LocalLoader  # NoQA
from piecutter.loaders.proxy import TextLoader, FileObjLoader, ProxyLoader  # NoQA
# Cutters.
from piecutter.cutter import Cutter  # NoQA
# Template engines.
from piecutter.engines import Engine  # NoQA
from piecutter.engines.django import DjangoEngine  # NoQA
from piecutter.engines.filename import FilenameEngine  # NoQA
from piecutter.engines.jinja import Jinja2Engine  # NoQA
from piecutter.engines.pythonformat import PythonFormatEngine  # NoQA
from piecutter.engines.proxy import ProxyEngine  # NoQA
# Writers.
from piecutter.writers import Writer  # NoQA
from piecutter.writers import PrintWriter  # NoQA
from piecutter.writers import StreamWriter  # NoQA
from piecutter.writers import TransparentWriter  # NoQA
