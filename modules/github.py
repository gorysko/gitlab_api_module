#! /usr/bin/env python

# github api docs could be found here
# https://developer.github.com/v3/

"""Github api module."""
from math import log

from .utils import add_query
from .utils import check_type
from .utils import urlbuilder
from .utils import helper

class GithubApi(object):
    """github api class."""

    def __init__(self, url, user, client_id, client_secret):
        """
        Args:
            user: user name, as string
            url: github api url
        """
        self._url = url
        self._user = user
        self._token = {'client_id': client_id, 'client_secret': client_secret}


    def get_orgs_events(self, org):
        """Gets lists of organization's events.
        Args:
            org: user organiztion id, as int.
        """
        org_id = check_type(org)

        return helper(add_query(urlbuilder(self._url[:-1], 'users', self._user,
                                  'events', 'orgs', org_id), self._token))

    def get_org_members(self, org):
        """Get lists of organization's public events.

        Args
           org: user organization id,  as int.
        """
        org_id = check_type(org)
        return helper(add_query(urlbuilder(self._url[:-1], 'orgs',
                      org_id, 'events'), self._token))

    def get_orgs(self):
        """Gets user organiztions."""
        return helper(add_query(urlbuilder(self._url[:-1], 'users',
                      self._user, 'orgs'), self._token))

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
        return helper(add_query(url, self._token))

    def get_orgs_membership(self):
        """Gets lists of user membership in organizations."""
        return helper(add_query(urlbuilder(self._url[:-1], self._user,
                                  'memberships', 'orgs'), self._token))

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
        return helper(add_query(url, self._token))

    def get_team(self, org, team):
        """Gets team by id.

        Args:
            org: organization id , as int
            team: team id in organization, as int.
        """
        org_id = check_type(org)
        team_id = check_type(team)

        return helper(add_query(urlbuilder(self._url[:-1], 'orgs', org_id,
                                 'teams', team_id), self._token))

    def get_user_repos(self):
        """Gets user repos."""
        return helper(add_query(urlbuilder(self._url[:-1], 'users',
                                self._user, 'repos'), self._token))

    def user_repo_info(self):
        """info"""
        repos = self.get_user_repos()
        forks = sum([item['forks'] for item in repos])
        owner = sum([item['fork'] for item in repos])
        contrib = len(self.repos_contributed_to())
        return repos, forks, owner, contrib

    def get_user_repos_names(self):
        """Gets user repos name."""
        return [item['name'] for item in self.get_user_repos()]

    def get_user_events(self):
        """Gets user events."""
        return helper(add_query(urlbuilder(self._url[:-1], 'users',
                                 self._user, 'received_events'), self._token))

    def get_user_public_events(self):
        """Gets user public_events."""
        return helper(add_query(urlbuilder(self._url[:-1], 'users',
                                self._user, 'received_events', 'public'),
                                self._token))

    def get_user_repos_watched(self):
        """Gets user repositories watched."""
        return helper(add_query(urlbuilder(self._url[:-1], 'users',
                                 self._user, 'subscriptions'), self._token))


    def repos_contributed_to(self):
        """Gets not user's repositories"""
        repos_contr = []
        for item in self.get_user_repos_watched():
            if item['owner']['login'] != self._user:
                repos_contr.append(item)
        return repos_contr

    def get_user_gists(self):
        """Gets user gists."""
        return helper(add_query(urlbuilder(self._url[:-1], 'users',
                                 self._user, 'gists'), self._token))

    def get_org_repos(self, org):
        """Gets org repos.

        Args:
            org: organization id, as int.
        """
        org_id = check_type(org)
        return helper(add_query(urlbuilder(self._url[:-1], 'org',
                      org_id, 'repos'), self._token))

    def get_repo(self, repo):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
        """
        return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                      self._user, repo), self._token))

    def get_user_repo_commits_sha(self, repo):
        """Gets repository comits sha's by it's id.

        Args:
            repo: repositiory name, as string
        """
        return [item['sha'] for item in self.get_user_repo_commits(repo)]

    def get_user_repo_commits(self, repo):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
        """
        return helper(add_query(urlbuilder(self._url[:-1], 'repos', self._user,
                      repo, 'commits'), self._token, {'per_page': 10000}))

    def get_user_repo_commit(self, repo, sha):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
            sha: commit sha, as string
        """
        return helper(add_query(urlbuilder(self._url[:-1], 'repos', self._user,
                      repo, 'commits', sha), self._token))

    def repos_commits(self):
        """get repos and their commits"""
        repos = {}
        for name in self.get_user_repos_names():
            repos[name] = self.get_user_repo_commits_sha(name)
        return repos

    def repo_stats(self, repo, info='contributors'):
        """Gets repository by it's id.

        Args:
            repo: repositiory name, as string
        """
        if info in ('contributors', 'commit_activity', 'code_frequency',
                    'participation', 'punch_card'):
            return helper(add_query(urlbuilder(self._url[:-1],
                          'repos', self._user, repo, 'stats', info),
                          self._token))
        return []

    def get_deletions(self):
        """Gets number of deletions and additons by repo"""
        deletions = [['Repo', 'Additons', 'Deletions']]
        for name in self.get_user_repos_names():
            contrib = self.repo_stats(repo=name)
            for author in contrib:
                if author['author']['login'] == self._user:
                    deletion = 0
                    additon = 0
                    for item in  author['weeks']:
                        deletion += log(int(item['d']) + 1)
                        additon += log((item['a']) + 1)
                    deletions.append([name, additon, deletion])
        return deletions

    def commits_by_repo(self):
        """gets commits quanteti by repo"""
        commits = {}
        for name in self.get_user_repos_names():
            participation = self.repo_stats(repo=name, info='participation')
            if participation != []:
                commits[name] = sum(participation.get('owner', [0]))
        return commits

    def get_repo_info(self, repo, info='contributors'):
        """Gets repository contributors by repo id.

        Args:
            repo: repository name , as string.
        """
        if info in ('contributors', 'languages', 'tags',
                    'branches', 'collaborators'):
            return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                                     self._user, repo, info), self._token))
        return []

    def get_repo_branch(self, repo, branch):
        """Gets repo branch by branch id.

        Args:
            repo: repo name , as string.
            branch: branch name, as string.
        """
        return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                                 self._user, repo, branch), self._token))

    def get_repo_collaborator(self, repo, info):
        """Gets repo collaborator.

        Args:
            repo: repo name, as string.
        """
        if info in ('milestones', 'collaborators', 'events', 'subscribers',
            'issues', 'assignees', 'labels'):
            return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                          self._user, repo, info), self._token))
        return []

    def get_repo_issues_comments(self, repo):
        """Gets repository issues comments.

        Args:
            repo: repo name, as string.
        """
        return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                                self._user, repo, 'issues', 'comments'),
                                self._token))

    def get_repo_issue_info(self, repo, issue, info=None):
        """Gets repository issue comments.

        Args:
            repo: repo name, as string.
            issue: issue id, as int.
        """

        iss_id = check_type(issue)
        if info in ('comments', 'events', 'labels', 'events'):
            return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                                    self._user, repo, 'issues', iss_id, info),
                                    self._token))
        return []

    def get_repo_issue_milestone_labels(self, repo, issue):
        """Gets repository issue milestone labels.

        Args:
            repo: repo name, as string.
            issue: issue id, as int.
        """

        iss_id = check_type(issue)
        return helper(add_query(urlbuilder(self._url[:-1], 'repos',
                                 self._user, repo, 'milestone',
                                 iss_id, 'labels'), self._token))
