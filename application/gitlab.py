#! /usr/bin/env python

# gitlab api docs could be found here
# http://doc.gitlab.com/ce/api/README.html

"""Gitlab api module"""
from application.utils import add_query
from application.utils import check_type
from application.utils import urlbuilder
from application.utils import helper

class GitlabApi(object):
    """gitlab api class """

    def __init__(self, private_token, url):
        """
        Args:
            private_token: gitlab private token, as string
            url: gitlab api url, should be ended by '/api/v3/'
        """
        self._private_token = {'private_token': private_token}
        self._url = url

    # pylint: disable-msg=E1121
    def get_projects(self, archived='true', order_by='id',
                     sort='asc', owned=False):
        """Gets projects data as dict"""
        query = {'private_token': self._private_token,
                 'archived': archived,
                 'order_by': order_by,
                 'sort': sort}
        url = urlbuilder(self._url[:-1], 'projects')
        if owned:
            url = urlbuilder(url, 'owned')

        return helper(add_query(url, self._private_token, query))

    def get_projects_ids(self):
        """Gets all project ids"""
        projects = self.get_projects()
        return [item['id'] for item in projects]

    def get_project(self, project_id):
        """Gets project by project id"""
        project_id = check_type(project_id)
        return helper(add_query(urlbuilder(self._url[:-1], 'projects',
                                            project_id), self._private_token))

    def get_project_snippets(self, project_id):
        """Gets project snippets """
        project_id = check_type(project_id)
        return helper(add_query(urlbuilder(self._url[:-1], 'projects',
                                                 project_id, 'snippets'),
                                 self._private_token))

    def get_project_snippet(self, project_id, snippet_id, raw=False):
        """Gets project snippet by id"""
        project_id = check_type(project_id)
        snippet_id = check_type(snippet_id)

        url = urlbuilder(self._url[:-1], 'projects',
                         project_id, 'snippets', snippet_id)
        if raw:
            url = urlbuilder(url, 'raw')
        return helper(add_query(url, self._private_token))

    def get_project_info(self, project_id, info=None):
        """Gets repos of the project
        Args:
           project_id: id of the project
           info: info type which you wnat to obtaine
        """
        keys = {'trees': '/repository/tree/?',
                'tags': '/repository/tags/?',
                'files': '/repository/files/?',
                'commits': '/repository/commits/?',
                'contributors': '/repository/contributors/?',
                'events': 'events',
                'members': 'members',
                'hooks': 'hooks',
                'branches': 'branches'}

        if info in keys:
            project_id = check_type(project_id)
            return helper(add_query(urlbuilder(self._url[:-1],
                                                      'projects',
                                                      project_id,
                                                      keys.get(info)),
                                     self._private_token))
        return None

    def get_project_team_member(self, project_id, user_id):
        """gets project team member.
        Args:
            project_id: id of the project
            user_id: id of the user
        """
        project_id = check_type(project_id)
        user_id = check_type(user_id)
        return helper(add_query(urlbuilder(self._url[:-1], 'projects',
                                                 project_id, 'members',
                                                 user_id),
                                 self._private_token))

    def get_branch(self, project_id, branch):
        """Gets single branch of the project.

        Args:
            project_id: id of the project.
            brnahc: name of the branch
        """
        project_id = check_type(project_id)
        return helper(add_query(urlbuilder(self._url[:-1], 'projects',
                                                 project_id, 'repository',
                                                 branch),
                                 self._private_token))

    def get_merge(self, project_id, sort='asc',
                  order_by='created_at', state='all'):
        """Gets list of merge requests.

        Args:
            project_id: id of the project.
            sort: type of sorting, default ascending
            order_by: ordering by created_at or updated_at fields.
            state: type of merges  all, merged, opened or closed
        """
        query = {'private_token': self._private_token,
                 'state': state,
                 'order_by': order_by,
                 'sort': sort}

        url = urlbuilder(self._url[:-1], 'projects', project_id)
        return helper(add_query(url, self._private_token, query))

    # Disabling too many args warning
    # pylint: disable-msg=R0913
    def get_project_issue(self, project_id, sort='asc', order_by='created_at',
                          state='all', labels='', milestones=''):
        """Gets list of merge requests.

        Args:
            project_id: id of the project.
            sort: type of sorting, default ascending
            order_by: ordering by created_at or updated_at fields.
            state: state: opened/closed
            labels: label of the issue
            milestone: milestone title
        """
        query = {'private_token': self._private_token,
                 'state': state,
                 'order_by': order_by,
                 'sort': sort,
                 'labels': labels,
                 'milestones': milestones}

        url = urlbuilder(self._url[:-1], 'projects', project_id, 'issues')
        return helper(add_query(url, self._private_token, query))

    def get_issue(self, sort='asc', order_by='created_at',
                  state='all', labels=''):
        """Gets list of merge requests.

        Args:
            sort: type of sorting, default ascending
            order_by: ordering by created_at or updated_at fields.
            state: opened/closed
            labels: label of the issue
        """
        query = {'private_token': self._private_token,
                 'state': state,
                 'order_by': order_by,
                 'sort': sort,
                 'labels': labels}

        return helper(add_query(urlbuilder(self._url[:-1], 'issues'),
                      self._private_token, query))

    def get_commit(self, project_id, commit_sha):
        """Gets commit info."""
        project_id = check_type(project_id)
        return helper(add_query(urlbuilder(self._url[:-1], 'projects',
                                                 project_id, 'repository',
                                                 'commits', commit_sha),
                                 self._private_token))

    def get_events(self, project_id):
        """Get project events by project_id"""
        project_id = check_type(project_id)
        return helper(add_query(urlbuilder(self._url[:-1], 'projects',
                                                 project_id, 'events'),
                                 self._private_token))

    def get_members(self, project_id):
        """gets project members by project_id"""
        project_id = check_type(project_id)
        return helper(add_query(urlbuilder(self._url[:-1],
                                                 'projects', project_id,
                                                 'members'),
                                 self._private_token))

    def users(self):
        """Gets list of users"""
        return helper(add_query(urlbuilder(self._url[:-1], 'users'),
                                 self._private_token))

    def keys(self):
        """Gets list of users"""
        return helper(add_query(urlbuilder(self._url[:-1], 'users', 'keys'),
                                 self._private_token))

    def get_user(self, user_id):
        """Gets user by it's id"""
        user_id = check_type(user_id)
        return helper(add_query(urlbuilder(self._url[:-1],
                                                 'users', user_id),
                                 self._private_token))

    def get_user_keys(self, user_id):
        """Gets user ssh keys"""
        user_id = check_type(user_id)
        return helper(add_query(urlbuilder(self._url[:-1],
                                                 'users', user_id, 'keys'),
                                 self._private_token))
