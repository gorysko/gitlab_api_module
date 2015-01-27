#! /usr/bin/env python

# github api docs could be found here
# https://developer.github.com/v3/

"""Github api module."""

from gitlab_api.application.utils import check_type
from gitlab_api.application.utils import urlbuilder
from gitlab_api.application.utils import helper

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
        return helper(urlbuilder(self._url[:-1], 'users', self._user, 'orgs'))

    def get_org_info(self, org, info=None):
        """Get organization members.

        Args
           org: user organization id,  as int.
        """
        org_id = check_type(org)
        if info is None:
            url = urlbuilder(self._url[:-1], 'orgs', org_id)
        elif info in ('members', 'public_members', 'teams', 'hooks'):
            url = urlbuilder(self._url[:-1], 'orgs', org_id, info)
        else:
            return None
        return helper(url)

    def get_orgs_membership(self):
        """Gets lists of user membership in organizations."""
        return helper(urlbuilder(self._url[:-1], self._user,
                                  'memberships', 'orgs'))

    def get_team_info(self, org, team, info=None):
        """Gets team members.

        Args:
            org: organization id, as int
            team: team id in orgznization , as int
        """

        org_id = check_type(org)
        team_id = check_type(team)
        if info is None:
            url = urlbuilder(self._url[:-1], 'orgs', org_id, 'teams', team_id)
        elif info in ('members', 'repos'):
            url = urlbuilder(self._url[:-1], 'orgs', org_id, 'teams',
                                      team_id, info)
        else:
            return None
        return helper(url)

    def get_user_repos(self):
        """Gets user repos."""
        return helper(urlbuilder(self._url[:-1], 'users',
                                  self._user, 'repos'))

    def get_org_repos(self, org):
        """Gets org repos.

        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)
        return helper(urlbuilder(self._url[:-1], 'org', org_id, 'repos'))

    def get_repo(self, repo):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
        """
        return helper(urlbuilder(self._url[:-1], 'repos', self._user, repo))

    def get_repo_info(self, repo, info='contributors'):
        """Gets repository contributors by repo id.

        Args:
            repo: repository name , as string.
        """
        if info in ('contributors', 'languages', 'tags',
                    'branches', 'collaborators'):
            return helper(urlbuilder(self._url[:-1], 'repos',
                                      self._user, repo, info))
        return None

    def get_repo_branch(self, repo, branch):
        """Gets repo branch by branch id.

        Args:
            repo: repo name , as string.
            branch: branch name, as string.
        """
        return helper(urlbuilder(self._url[:-1], 'repos',
                                  self._user, repo, branch))

    def get_repo_collaborator(self, repo):
        """Gets repo collaborator.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder(self._url[:-1], 'repos', self._user, repo,
                                  'collaborators'))
