#! /usr/bin/env python

"""Additional utils for correct work."""
from json import loads
from urllib import urlencode
from urllib2 import urlopen

def return_result(response):
    """Reads and checks response"""
    if response is not None:
        result = response.read()
        if result is not None:
            return loads(result)
    return None


def check_type(item):
    """Checks and casts type of item"""
    if type(item) == int:
        return str(item)
    return item


def urlbuilder(*args):
    """Builds correct url."""
    return '/'.join(args)


def helper(url):
    """helper"""
    try:
        response = urlopen(url)
        if response is not None:
            return return_result(response)
    except:
        return []

def add_query(url, token, data=None):
    """Adds query to url"""
    if url is not None:
        if data is None:
            data = {}
        data.update(token)
        query = urlencode(data)
        print url + '?' + query
        return url + '?' + query
    return ''