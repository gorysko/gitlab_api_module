#! /usr/bin/env python

# github api docs could be found here
# https://developer.github.com/v3/

"""Github api module."""

from urllib import urlopen

from utils import return_result

class GithubApi(object):
    """github api class."""

    def __init__(self, url, user)
        """
        Args:
            user: user name, as string
            url: github api url
        """
        self._url = url
        self._user = user

    def get_orgs(self):
        """Gets user organiztions."""
        url = self._url + 'users/' + user + '/orgs'
        response = urlopen(url)
        return return_result(response)

    def get_org(self, org):
        """Get user org.

        Args:
            org: user organization id, as int
        """
        org_id = check_type(org)

        url = self._url + 'users/' + user + '/orgs/' + org_id
        response = urlopen(url)
        return return_result(response)