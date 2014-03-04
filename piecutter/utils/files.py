# -*- coding: utf-8 -*-
"""Manage temporary directories."""
import os
import shutil
import tempfile


class temporary_directory(object):
    """Create, yield, and finally delete a temporary directory.

    >>> with temporary_directory() as directory:
    ...     os.path.isdir(directory)
    True
    >>> os.path.exists(directory)
    False

    Deletion of temporary directory is recursive.

    >>> with temporary_directory() as directory:
    ...     filename = os.path.join(directory, 'sample.txt')
    ...     __ = open(filename, 'w').close()
    ...     os.path.isfile(filename)
    True
    >>> os.path.isfile(filename)
    False

    """
    def __enter__(self):
        """Create temporary directory and return its path."""
        self.path = tempfile.mkdtemp()
        return self.path

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        """Remove temporary directory recursively."""
        try:
            shutil.rmtree(self.path)
        except OSError:
            pass


class chdir(object):
    """Context manager that change current working directory."""
    def __init__(self, new_dir):
        #: Remember previous value of os.getcwd().
        self.previous_dir = os.getcwd()
        #: New directory.
        self.new_dir = new_dir

    def __enter__(self):
        os.chdir(self.new_dir)

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        os.chdir(self.previous_dir)
