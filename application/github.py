#! /usr/bin/env python

# github api docs could be found here
# https://developer.github.com/v3/

"""Github api module."""

from utils import check_type
from utils import urlbuilder
from utils import helper

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
        return helper(urlbuilder([self._url[:-1], 'users', self._user, 'orgs']))

    def get_org(self, org):
        """Get user org.

        Args:
            org: user organization id, as int
        """
        org_id = check_type(org)
        return helper(urlbuilder([self._url, 'orgs', org_id]))

    def get_org_members(self, org):
        """Get organization members.

        Args
           org: user organization id,  as int.
        """
        org_id = check_type(org)
        return helper(urlbuilder([self._url[:-1], 'orgs', org_id, 'members']))


    def get_public_members(self, org):
        """Gets public members of the organization.
        Args:
            org: user organiztion id, as int.
        """
        org_id = check_type(org)

        return helper(urlbuilder([self._url[:-1], 'users',
                                  self._user, 'orgs', org_id,
                                  'public_members']))

    def get_orgs_membership(self):
        """Gets lists of user membership in organizations."""
        return helper(urlbuilder([self._url[:-1], 'users', self._user,
                                  'memberships', 'orgs']))

   def get_orgs_events(self, org):
        """Gets lists of organization's events.
        Args:
            org: user organiztion id, as int.
        """
        org_id = check_type(org)

        return helper(urlbuilder([self._url[:-1], 'users', self._user,
                                  'events', 'orgs', org_id]))

    def get_org_members(self, org):
        """Get lists of organization's public events.

        Args
           org: user organization id,  as int.
        """
        org_id = check_type(org)
        return helper(urlbuilder([self._url[:-1], 'orgs', org_id, 'events']))

    def get_teams(self, org):
        """Gets list of teams.
        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)

        return helper(urlbuilder([self._url[:-1], 'users', self._user, 'orgs',
                                  org_id, 'teams']))

    def get_team(self, org, team):
        """Gets team by id.

        Args:
            org: organization id , as int
            team: team id in organization, as int.
        """
        org_id = check_type(org)
        team_id = check_type(team)

        return helper(urlbuilder([self._url[:-1], 'orgs', org_id,
                                  'teams', team_id]))

    def get_team_info(self, org, team, detail='members'):
        """Gets team members.

        Args:
            org: organization id, as int
            team: team id in orgznization , as int
        """

        org_id = check_type(org)
        team_id = check_type(team)
        if detail in ('members', 'repos'):
            return helper(urlbuilder([self._url[:-1], 'orgs', org_id, 'teams',
                                      team_id, detail]))
        return None

    def get_user_repos(self):
        """Gets user repos."""
        return helper(urlbuilder([self._url[:-1], 'users',
                                  self._user, 'repos']))

    def get_user_events(self):
        """Gets user events."""
        return helper(urlbuilder([self._url[:-1], 'users',
                                  self._user, 'received_events']))

    def get_user_public_events(self):
        """Gets user public_events."""
        return helper(urlbuilder([self._url[:-1], 'users',
                                  self._user, 'received_events', 'public']))

    def get_user_repos_watched(self):
        """Gets user repositories watched."""
        return helper(urlbuilder([self._url[:-1], 'users',
                                  self._user, 'subscriptions']))

    def get_user_gists(self):
        """Gets user gists."""
        return helper(urlbuilder([self._url[:-1], 'users',
                                  self._user, 'gists']))

    def get_org_repos(self, org):
        """Gets org repos.

        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)
        return helper(urlbuilder([self._url[:-1], 'org', org_id, 'repos']))

    def get_repo(self, repo):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
        """
        return helper(urlbuilder([self._url[:-1], 'repos', self._user, repo]))

    def get_repo_info(self, repo, info='contributors'):
        """Gets repository contributors by repo id.

        Args:
            repo: repository name , as string.
        """
        if info in ('contributors', 'languages', 'tags',
                    'branches', 'collaborators'):
            return helper(urlbuilder([self._url[:-1], 'repos',
                                      self._user, repo, info]))
        return None

    def get_repo_branch(self, repo, branch):
        """Gets repo branch by branch id.

        Args:
            repo: repo name , as string.
            branch: branch name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, branch]))

    def get_repo_collaborator(self, repo):
        """Gets repo collaborator.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos', self._user, repo,
                                  'collaborators']))

    def get_repo_events(self, repo):
        """Gets repository events.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'events']))

    def get_repo_watchers(self, repo):
        """Gets repository watchers.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'subscribers']))

    def get_repo_issues(self, repo):
        """Gets repository issues.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'issues']))

    def get_repo_assignees(self, repo):
        """Gets repository assignees.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'assignees']))

    def get_repo_issues_comments(self, repo):
        """Gets repository issues comments.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'issues', 'comments']))

    def get_repo_issue_comments(self, repo, issue):
        """Gets repository issue comments.

        Args:
            repo: repo name, as string.
            issue: issue id, as int.
        """

        iss_id = check_type(issue)
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'issues', iss_id, 'comments']))

    def get_repo_issue_events(self, repo, issue):
        """Gets repository issue events.

        Args:
            repo: repo name, as string.
            issue: issue id, as int.
        """

        iss_id = check_type(issue)
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'issues', iss_id, 'events']))

    def get_repo_issues_events(self, repo):
        """Gets repository issues events.

        Args:
            repo: repo name, as string.
        """

        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'issues', 'events']))

    def get_repo_labels(self, repo):
        """Gets all repository labels.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'labels']))

    def get_repo_issue_labels(self, repo, issue):
        """Gets repository issue labels.

        Args:
            repo: repo name, as string.
            issue: issue id, as int.
        """

        iss_id = check_type(issue)
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'issues', iss_id, 'labels']))

    def get_repo_issue_milestone_labels(self, repo, issue):
        """Gets repository issue milestone labels.

        Args:
            repo: repo name, as string.
            issue: issue id, as int.
        """

        iss_id = check_type(issue)
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'milestone', iss_id, 'labels']))

    def get_repo_milestones(self, repo):
        """Gets all repository milestones.

        Args:
            repo: repo name, as string.
        """
        return helper(urlbuilder([self._url[:-1], 'repos',
                                  self._user, repo, 'milestones']))
