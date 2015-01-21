#! /usr/bin/env python

# github api docs could be found here
# https://developer.github.com/v3/

"""Github api module."""

from urllib import urlopen

from utils import return_result
from utils import check_type

class GithubApi(object):
    """github api class."""

    def __init__(self, url, user):
        """
        Args:
            user: user name, as string
            url: github api url
        """
        self._url = url
        self._user = user

    def get_orgs(self):
        """Gets user organiztions."""
        url = self._url + 'users/' + self._user + '/orgs'

        return self._helper(url)

    def get_org(self, org):
        """Get user org.

        Args:
            org: user organization id, as int
        """
        org_id = check_type(org)

        url = self._url + 'orgs/' + org_id

        return self._helper(url)

    def get_org_members(self, org):
        """Get organization members.

        Args
           org: user organization id,  as int.
        """
        org_id = check_type(org)

        url = self._url + 'orgs/' +  org_id + '/members/'

        return self._helper(url)


    def get_public_members(self, org):
        """Gets public members of the organization.
        Args:
            org: user organiztion id, as int.
        """
        org_id = check_type(org)

        url = self._url + 'users/' + self._user + '/orgs/' + \
              org_id + '/public_members/'

        return self._helper(url)

    def get_orgs_membership(self):
        """Gets lists of user membership in organizations."""

        url = self._url + 'users/' + self._user + '/memberships/orgs'

        return self._helper(url)

    def get_teams(self, org):
        """Gets list of teams.
        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)

        url = self._url + 'users/' + self._user + '/orgs/' + org_id + '/teams/'

        return self._helper(url)

    def get_team(self, org, team):
        """Gets team by id.

        Args:
            org: organization id , as int
            team: team id in organization, as int.
        """
        org_id = check_type(org)
        team_id = check_type(team)

        url = self._url + 'orgs/' + org_id + '/teams/' + team_id

        return self._helper(url)

    def get_team_members(self, org, team):
        """Gets team members.

        Args:
            org: organization id, as int
            team: team id in orgznization , as int
        """

        org_id = check_type(org)
        team_id = check_type(team)

        url = self._url + 'orgs/' + org_id + '/teams/' + team_id + '/members/'

        return self._helper(url)

    def get_team_repos(self, org, team):
        """Gets team repos in organization.

        Args:
            org: organization id, as int
            team: team id in organizatin, as int
        """
        org_id = check_type(org)
        team_id = check_type(team)

        url = self._url + 'orgs/' + org_id + '/teams/' + team_id + '/repos/'

        return self._helper(url)

    def get_user_repos(self):
        """Gets user repos."""

        url = self._url + 'users/' + self._user + '/repos/'

        return self._helper(url)

    def get_org_repos(self, org):
        """Gets org repos.

        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)
        url = self._url + 'org/' + org_id + '/repos/'

        return self._helper(url)

    def get_repo(self, repo):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
        """
        url = self._url + 'repos/' + self._user + '/' + repo

        return self._helper(url)

    def get_repo_info(self, repo, info='contributors'):
        """Gets repository contributors by repo id.

        Args:
            repo: repository name , as string.
        """
        if info in ('contributors', 'languages', 'tags',
                    'branches', 'collaborators'):
            url = self._url + 'repos/' + self._user + '/' + repo + '/' + info

            return self._helper(url)
        return None

    def get_repo_branch(self, repo, branch):
        """Gets repo branch by branch id.

        Args:
            repo: repo name , as string.
            branch: branch name, as string.
        """
        url = self._url + 'repos/' + self._user + '/' + repo + '/' + branch
        return self._helper(url)

    def get_repo_collaborator(self, repo):
        """Gets repo collaborator.

        Args:
            repo: repo name, as string.
        """
        url = self._url + 'repos/' + self._user + '/' + repo + '/' + \
              'collaborators'
        return self._helper(url)

    @staticmethod
    def _helper(url):
        """helper"""
        response = urlopen(url)
        if response is not None:
            return return_result(response)
        return None
