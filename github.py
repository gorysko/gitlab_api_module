#! /usr/bin/env python

# github api docs could be found here
# https://developer.github.com/v3/

"""Github api module."""

from urllib import urlopen

class GithubApi(object):
    """github api class."""

    def __init__(self, url, user)
        """
        Args:
            user: user name, as string
            url: github api url
        """
        self._ulr = url
        self._user = user

    def get_orgs(self):
        """Gets user organiztions."""
        url = self._url + 'users/' + user + '/orgs'
        response = urlopen(url)
