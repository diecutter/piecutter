# -*- coding: utf-8 -*-
"""Execution control."""


class BreakOnResult(Exception):
    """Special exception to break dispatch loop on result."""
    def __init__(self, result):
        self.result = result


#: Sentinel to distinguish callables that return ``None`` and those that
#: return no result.
NO_RESULT = object()


def is_result(result):
    """Return ``True`` if result is not ``None`` and not :data:`NO_RESULT`."""
    if result is None:
        return False
    if result is NO_RESULT:
        return False
    return True


class Dispatcher(object):
    def __init__(self, runners=[]):
        #: Iterator on callables to dispatch.
        self.runners = runners


class FirstResultDispatcher(Dispatcher):
    """A dispatcher that returns the first result got from callables."""
    def __call__(self, *args, **kwargs):
        for runner in self.runners:
            result = runner(*args, **kwargs)
            if is_result(result):
                return result


class LastResultDispatcher(Dispatcher):
    """A dispatcher that returns last result got from callables, same args."""
    def __init__(self, runners=[]):
        super(LastResultDispatcher, self).__init__(runners)

        #: Remember the result.
        self.result = None

    def __call__(self, *args, **kwargs):
        for runner in self.runners:
            result = runner(*args, **kwargs)
            if is_result(result):
                self.result = result
        return self.result


class ChainDispatcher(Dispatcher):
    def __call__(self, *args, **kwargs):
        result = args[0]
        for runner in self.runners:
            result = runner(result)
        return result
