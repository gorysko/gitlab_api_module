#! /usr/bin/env python

# gitlab api docs could be found here
# http://doc.gitlab.com/ce/api/README.html

"""Gitlab api module"""
from json import loads
from urllib import urlencode
from urllib2 import urlopen

class GitlabApi(object):
    """gitlab api class """

    def __init__(self, private_token, url):
        """
        Args:
            private_token: gitlab private token, as string
            url = gitlab api url, should be ended by '/api/v3/'
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
        response = urlopen(url + post_query)
        return self._return_result(response)

    def get_projects_ids(self):
        """Gets all project ids"""
        projects = self.get_projects()
        return [item['id'] for item in projects]

    def get_project(self, project_id):
        """Gets project by project id"""
        project_id = self._check_type(project_id)

        url = self._url + 'projects/' + project_id + '?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        response = urlopen(url + post_query)
        return self._return_result(response)

    def get_project_snippets(self, project_id):
        """Gets project snippets """
        project_id = self._check_type(project_id)

        url = self._url + 'projects/' + project_id + '/snippets/?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        response = urlopen(url + post_query)
        return self._return_result(response)

    def get_project_snippet(self, project_id, snippet_id, raw=False):
        """Gets project snippet by id"""
        project_id = self._check_type(project_id)
        snippet_id = self._check_type(snippet_id)

        url = self._url + 'projects/' + project_id + '/snippets/' + \
              snippet_id + '?'
        if raw:
            url = url[:-1] + 'raw' +'?'

        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        response = urlopen(url + post_query)
        return self._return_result(response)

    def get_repo_info(self, project_id, info=0):
        """Gets repos of the project"""
        if info in (0, 1, 2):
            project_id = self._check_type(project_id)
            end =  '/repository/tree/?'

            if info == 1:
                end =  '/repository/tags/?'

            if info == 2:
                end = '/repository/contributors/?'

            url = self._url + 'projects/' + project_id + end

            query = {'private_token': self._private_token}
            post_query = urlencode(query)

            response = urlopen(url + post_query)
            return self._return_result(response)


    def get_events(self, project_id):
        """Get project events by project_id"""
        project_id = self._check_type(project_id)

        url = self._url + 'projects/' + project_id + '/' + 'events?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        response = urlopen(url + post_query)
        return self._return_result(response)

    def get_members(self, project_id):
        """gets project members by project_id"""
        project_id = self._check_type(project_id)

        url = self._url + 'projects/' + project_id + '/' + 'members?'
        query = {'private_token': self._private_token}
        post_query = urlencode(query)

        response = urlopen(url + post_query)
        return self._return_result(response)

    def users(self):
        """Gets list of users"""
        response = urlopen(self._url + 'users?' + self._private_token)
        return self._return_result(response)

    def get_user(self, user_id):
        """Gets user by it's id"""
        user_id = self._check_type(user_id)
        response = urlopen(self._url + 'users/' + user_id + '?' + \
                           self._private_token)
        return self._return_result(response)

    def get_user_keys(self, user_id):
        """Gets user ssh keys"""
        user_id = self._check_type(user_id)

        response = urlopen(self._url + 'users/' + user_id + '/keys' + '?' + \
                           self._private_token)
        return self._return_result(response)

    @staticmethod
    def _return_result(response):
        """Reads and checks response"""
        if response is not None:
            result = response.read()
            if result is not None:
                return loads(result)
        return None

    @staticmethod
    def _check_type(item):
        """Checks and casts type of item"""
        if type(item) == int:
            return str(item)
        return item
