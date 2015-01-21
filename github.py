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
        response = urlopen(url)
        return return_result(response)

    def get_org(self, org):
        """Get user org.

        Args:
            org: user organization id, as int
        """
        org_id = check_type(org)

        url = self._url + 'orgs/' + org_id
        response = urlopen(url)
        return return_result(response)

    def get_org_members(self, org):
        """Get organization members.

        Args
           org: user organization id,  as int.
        """
        org_id = check_type(org)

        url = self._url + 'orgs/' +  org_id + '/members/'
        response = urlopen(url)
        return return_result(response)


    def get_public_members(self, org):
        """Gets public members of the organization.
        Args:
            org: user organiztion id, as int.
        """
        org_id = check_type(org)

        url = self._url + 'users/' + self._user + '/orgs/' + \
              org_id + '/public_members/'

        response = urlopen(url)
        return return_response(response)

    def get_orgs_membership(self):
        """Gets lists of user membership in organizations."""

        url = self._url + 'users/' + self._user + '/memberships/orgs'

        response = urlopen(url)
        return return_result(response)

    def get_teams(self, org):
        """Gets list of teams.
        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)

        url = self._url + 'users/' + self._user + '/orgs/' + org_id + '/teams/'

        response = urlopen(url)
        return return_result(response)

    def get_team(self, org, team):
        """Gets team by id.

        Args:
            org: organization id , as int
            team: team id in organization, as int.
        """
        org_id = check_type(org)
        team_id = check_type(team)

        url = self._url + 'orgs/' + org_id + '/teams/' + team_id

        response = urlopen(url)
        return return_response

    def get_team_members(self, org, team):
        """Gets team members.

        Args:
            org: organization id, as int
            team: team id in orgznization , as int
        """

        org_id = check_type(org)
        team_id = check_type(team)

        url = self._url + 'orgs/' + org_id + '/teams/' + team_id + '/members/'

        response = urlopen(url)
        return return_result(response)

    def get_team_repos(self, org, team):
        """Gets team repos in organization.

        Args:
            org: organization id, as int
            team: team id in organizatin, as int
        """
        org_id = check_type(org)
        team_id = check_type(team)

        url = self._url + 'orgs/' + org_id + '/teams/' + team_id + '/repos/'

        response = urlopen(url)
        return return_result(response)

    def get_user_repos(self):
        """Gets user repos."""

        url = self._url + 'users/' + self._user + '/repos/'

        response = urlopen(url)
        return return_result(result)

    def get_org_repos(self, org):
        """Gets org repos.

        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)
        url = self._url + 'org/' + org_id + '/repos/'

        response = urlopen(url)
        return return_result(reposonse)

    def get_repo(self, repo):
        """Gets repository by it's id.

        Args:
            repo: repositiory id, as int.
        """
        repo_id = check_type(repo)

        url = self._url + 'repos/' + self._user + '/' + repo_id

        response = urlopen(url)
        return return_result(response)

    def get_repo_info(self, repo, info='contributors'):
        """Gets repository contributors by repo id.

        Args:
            repo: repository id , as int.
        """
        if info in ('contributors', 'languages', 'tags', 'branches'):
            repo_id = check_type(repo)
            url = self._url + 'repos/' + self._user + '/' + \
                  repo_id + '/' + info

            response = urlopen(url)
            return return_result(response)
        return None