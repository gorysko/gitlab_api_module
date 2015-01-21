#! /usr/bin/env python

"""Additional utils for correct work."""


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