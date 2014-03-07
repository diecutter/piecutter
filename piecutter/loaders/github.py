# -*- coding: utf-8 -*-
"""Manage templates located on Github."""
import os
import tarfile

import requests

from piecutter.exceptions import TemplateNotFound
from piecutter.resources import FileResource, DirResource


class GithubLoader(object):
    """Loads resources from Github."""
    def __init__(self, checkout_dir):
        self.checkout_dir = checkout_dir

    def get_resource(self, engine, filename_engine, user, project, commit,
                     path):
        """Return resource (either a file or directory)."""
        local_root = self.github_targz(user, project, commit)
        local_path = os.path.join(local_root,
                                  '{project}-{commit}'.format(project=project,
                                                              commit=commit),
                                  path)
        if os.path.isdir(local_path):
            resource = DirResource(path=local_path, engine=engine,
                                   filename_engine=filename_engine)
        else:
            resource = FileResource(path=local_path, engine=engine,
                                    filename_engine=filename_engine)
        return resource

    def github_targz(self, user, project, commit):
        """Download archive from Github and return path to local extract."""
        try:
            return self._checkout
        except AttributeError:
            url = self.github_targz_url(user, project, commit)
            archive = tarfile.open(fileobj=self.github_targz_content(url),
                                   mode='r|gz')
            archive.extractall(self.checkout_dir)
            self._checkout = self.checkout_dir
            return self._checkout

    def github_targz_content(self, url):
        """Return stream from URL."""
        try:
            response = requests.get(url, stream=True)
        except requests.exceptions.RequestException as e:
            raise e
        if response.status_code == 404:
            raise TemplateNotFound(url)
        return response.raw

    def github_targz_url(self, user, project, commit):
        """Return URL of Github archive.

        >>> from piecutter.utils import temporary_directory
        >>> with temporary_directory() as temp_dir:
        ...     loader = GithubLoader(temp_dir)
        ...     loader.github_targz_url('user', 'project', 'master')
        'https://codeload.github.com/user/project/tar.gz/master'

        """
        return 'https://codeload.github.com/{user}/{project}/tar.gz/{commit}' \
               .format(user=user, project=project, commit=commit)
