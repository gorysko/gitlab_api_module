"""Gitlab api module"""
from urllib2 import urlopen
from urllib import urlencode

PRIVATE_TOKEN = 'your token'
URL = 'https://git.corp.sethq.com/api/v3/'


def projects(archived='true', order_by='id', sort='asc'):
    """Gets projects data as dict"""
    url = URL + 'projects?'

    query = {'private_token': PRIVATE_TOKEN,
             'archived': archived,
             'order_by': order_by,
             'sort': sort}

    post_query = urlencode(query)
    response = urlopen(url + post_query)
    return _return_result(response)


def get_project(project_id):
    """Gets project by project id"""
    project_id = _check_type(project_id)
    url = URL + 'projects/' + project_id + '?'

    query = {'private_token': PRIVATE_TOKEN}
    post_query = urlencode(query)

    response = urlopen(url + post_query)
    return _return_result(response)


def users():
    """Gets list of users"""
    response = urlopen(URL + 'users?' + PRIVATE_TOKEN)
    return _return_result(response)


def get_user(user_id):
    """Gets user by it's id"""
    user_id = _check_type(user_id)
    response = urlopen(URL + 'users/' + user_id + '?' + PRIVATE_TOKEN)
    return _return_result(response)


def get_user_keys(user_id):
    """Gets user ssh keys"""
    user_id = _check_type(user_id)
    response = urlopen(URL + 'users/' + user_id + '/keys' + '?' + PRIVATE_TOKEN)
    return _return_result(response)

def _return_result(response):
    """Reads and checks response"""
    result = response.read()
    if result is not None:
        return result
    return None


def _check_type(item):
    """Checks and casts type of item"""
    if type(item) == int:
        return str(item)
    return item

if __name__ == '__main__':
    print get_project(141)
