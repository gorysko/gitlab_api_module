"""Congfiguration module."""

SECRET_KEY = 'development key'
DEBUG = True

FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"
PAGE_DATE_FORMAT_STR = "%d-%m-%y"
DISPLAY_DATE_FORMAT_STR = "%d-%m-%y"
FREEZER_IGNORE_MIMETYPE_WARNINGS = True
FREEZER_DEFAULT_MIMETYPE = "text/html"

GITHUB_CLIENT_ID = '5a80a178d27e64a4d264'
GITHUB_CLIENT_SECRET = '243aa848374960e115494977cada492466f47902'
GITHUB_BASE_URL = 'https://api.github.com/'
GITHUB_AUTH_URL = 'https://github.com/login/oauth/'


SQLALCHEMY_DATABASE_URI = 'sqlite:///github.db'

SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'