# -*- coding: utf-8 -*-
"""Tests around :py:mod:`piecutter.github`."""
import os
from StringIO import StringIO
import tarfile
import unittest
try:
    from unittest import mock
except ImportError:
    import mock

import pyramid.exceptions
import requests

from piecutter.utils import temporary_directory
import piecutter.github


class GithubLoaderTestCase(unittest.TestCase):
    """Tests around :py:class:`piecutter.github.GithubLoader`."""

    def setup_targz(self, path, project, commit):
        """Create archive file in ``path``."""
        with tarfile.open(path, mode='w:gz') as archive:
            greetings_content = 'Hello {name}!'
            greetings_file = StringIO(greetings_content)
            greetings_name = '{project}-{commit}/greetings.txt'.format(
                project=project, commit=commit)
            greetings_info = tarfile.TarInfo(name=greetings_name)
            greetings_info.size = len(greetings_content)
            greetings_info.type = tarfile.REGTYPE
            archive.addfile(greetings_info, fileobj=greetings_file)

    def test_github_targz(self):
        """github_targz downloads and extracts archive in directory."""
        with temporary_directory() as github_mock_dir:
            archive_name = os.path.join(github_mock_dir, 'foo.tar.gz')
            self.setup_targz(archive_name, 'piecutter', 'master')
            with open(archive_name, 'r') as archive:
                content_mock = mock.Mock(return_value=archive)
                with temporary_directory() as output_dir:
                    loader = piecutter.github.GithubLoader(output_dir)
                    loader.github_targz_content = content_mock
                    loader.github_targz('fake-user', 'piecutter', 'master')
                    self.assertTrue(
                        os.path.exists(os.path.join(output_dir,
                                                    'piecutter-master',
                                                    'greetings.txt')))

    def test_github_targz_content(self):
        """github_targz_content downloads and returns archive stream."""
        with temporary_directory() as github_mock_dir:
            archive_name = os.path.join(github_mock_dir, 'foo.tar.gz')
            self.setup_targz(archive_name, 'piecutter', 'master')
            with open(archive_name, 'r') as archive:
                response_mock = mock.MagicMock()
                response_mock.raw = archive
                response_mock.status_code = 200
                get_mock = mock.Mock(return_value=response_mock)
                with mock.patch('piecutter.github.requests.get', new=get_mock):
                    with temporary_directory() as output_dir:
                        loader = piecutter.github.GithubLoader(output_dir)
                        content = loader.github_targz_content('fake-url')
                        self.assertTrue(archive is content)

    def test_github_targz_error(self):
        """github_targz_content raises requests exceptions."""
        with temporary_directory() as github_mock_dir:
            archive_name = os.path.join(github_mock_dir, 'foo.tar.gz')
            self.setup_targz(archive_name, 'piecutter', 'master')
            get_mock = mock.Mock(
                side_effect=requests.exceptions.ConnectionError)
            with mock.patch('piecutter.github.requests.get', new=get_mock):
                with temporary_directory() as output_dir:
                    loader = piecutter.github.GithubLoader(output_dir)
                    self.assertRaises(
                        requests.exceptions.ConnectionError,
                        loader.github_targz_content,
                        'fake-url')

    def test_github_targz_content_not_found(self):
        """github_targz_content raises NotFound if Github returns 404."""
        with temporary_directory() as github_mock_dir:
            archive_name = os.path.join(github_mock_dir, 'foo.tar.gz')
            self.setup_targz(archive_name, 'piecutter', 'master')
            response_mock = mock.MagicMock()
            response_mock.status_code = 404
            get_mock = mock.Mock(return_value=response_mock)
            with mock.patch('piecutter.github.requests.get', new=get_mock):
                with temporary_directory() as output_dir:
                    loader = piecutter.github.GithubLoader(output_dir)
                    self.assertRaises(
                        pyramid.exceptions.NotFound,
                        loader.github_targz_content,
                        'fake-url')
