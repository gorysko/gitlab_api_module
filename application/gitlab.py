#! /usr/bin/env python

# gitlab api docs could be found here
# http://doc.gitlab.com/ce/api/README.html

"""Gitlab api module"""

from urllib import urlencode

from gitlab_api.application.utils import check_type
from gitlab_api.application.utils import urlbuilder
from gitlab_api.application.utils import helper

class GitlabApi(object):
    """gitlab api class """

    def __init__(self, private_token, url):
        """
        Args:
            private_token: gitlab private token, as string
            url: gitlab api url, should be ended by '/api/v3/'
        """
        self._private_token = private_token
        self._url = url

    def get_projects(self, archived='true', order_by='id', sort='asc'):
        """Gets projects data as dict"""
        url = self._url + 'projects?'

        query = {'private_token': self._private_token,
                 'archived': archived,
                 'order_by': order_by,
                 'sort': sort}

        post_query = urlencode(query)
        return helper(url + post_query)

    def get_projects_ids(self):
        """Gets all project ids"""
        projects = self.get_projects()
        return [item['id'] for item in projects]

    def get_project(self, project_id):
        """Gets project by project id"""
        project_id = check_type(project_id)

        url = self._url + 'projects/' + project_id + '?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        return helper(url + post_query)

    def get_project_snippets(self, project_id):
        """Gets project snippets """
        project_id = check_type(project_id)

        url = self._url + 'projects/' + project_id + '/snippets/?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        return helper(url + post_query)

    def get_project_snippet(self, project_id, snippet_id, raw=False):
        """Gets project snippet by id"""
        project_id = check_type(project_id)
        snippet_id = check_type(snippet_id)

        url = self._url + 'projects/' + project_id + '/snippets/' + \
              snippet_id + '?'
        if raw:
            url = url[:-1] + 'raw' +'?'

        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        return helper(url + post_query)

    def get_project_info(self, project_id, info=0):
        """Gets repos of the project
        Args:
           project_id: id of the project
           info: info type which you wnat to obtaine
        """
        if info in ('tags', 'trees', 'files', 'commits', 'contributors'):
            project_id = check_type(project_id)
            end = '/repository/tree/?'

            keys = {'trees': '/repository/tags/?',
                    'tags': '/repository/tags/?',
                    'files': '/repository/files/?',
                    'commits': '/repository/commits/?',
                    'contributors': '/repository/contributors/?'}

            end = keys.get(info, 'tags')

            url = self._url + 'projects/p' + project_id + end

            query = {'private_token': self._private_token}
            post_query = urlencode(query)

            return helper(url + post_query)
        return None

    def get_commit(self, project_id, commit_sha):
        """Gets commit info."""
        project_id = check_type(project_id)

        url = self._url + 'projects/' + project_id \
              + '/repository/commits/' + commit_sha + '?'

        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        return helper(url + post_query)

    def get_events(self, project_id):
        """Get project events by project_id"""
        project_id = check_type(project_id)

        url = self._url + 'projects/' + project_id + '/' + 'events?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        return helper(url + post_query)

    def get_members(self, project_id):
        """gets project members by project_id"""
        project_id = check_type(project_id)

        url = self._url + 'projects/' + project_id + '/' + 'members?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        return helper(url + post_query)

    def users(self):
        """Gets list of users"""
        return helper(urlbuilder(self._url, 'users?', self._private_token))

    def get_user(self, user_id):
        """Gets user by it's id"""
        user_id = check_type(user_id)
        return helper(self._url + 'users/' + user_id + \
                      '?' + self._private_token)

    def get_user_keys(self, user_id):
        """Gets user ssh keys"""
        user_id = check_type(user_id)

        return helper(self._url + 'users/' + user_id + \
                      '/keys' + '?' + self._private_token)
