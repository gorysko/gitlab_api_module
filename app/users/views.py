#! /usr/bin/env python
"""Server module, based on flask."""
from json import dumps
from json import loads

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import g
from flask import url_for
from flask import redirect
from flask_bootstrap import Bootstrap
from flask.ext.assets import Environment
from flask.ext.markdown import Markdown
from flask.ext.flatpages import FlatPages
from flask.ext.flatpages import pygments_style_defs
from flask.ext.github import GitHub

from users import User
from modules import github as git_wrapper

from app.config import GITHUB_CLIENT_ID
from app.config import GITHUB_CLIENT_SECRET
from app.config import GITHUB_BASE_URL
from app.config import GITHUB_AUTH_URL
from app.database import engine
from app.database import Base
from app.database import db_session


@app.route('/blog')
def blog():
    """Renders home page."""
    post_list = get_pages_by_type('post')
    latest = sorted(post_list, reverse=True, key=lambda p: p.meta['date'])
    return render_template('blog.html', user=g.user_metadata, posts=latest[:5])


@app.route('/stats', methods=['GET'])
def stats(name=None):
    data = [['Type of repos', 'Number of items']]
    commits = [['Repo name', 'Number of commits']]
    deletions = []
    total_commits = 0

    if g.user_metadata is not None:
        git = git_wrapper.GithubApi(app.config['GITHUB_BASE_URL'],
              g.user_metadata['login'], app.config['GITHUB_CLIENT_ID'],
              app.config['GITHUB_CLIENT_SECRET'])

        if g.user_id.repo_commits is not None and \
            g.user_id.user_repo_info is not None and \
            g.user_id.deletions is not None:

            repo_commits = loads(g.user_id.repo_commits)
            info = loads(g.user_id.user_repo_info)
            deletions = loads(g.user_id.deletions)
        else:
            repo_commits = git.commits_by_repo()
            g.user_id.repo_commits = dumps(repo_commits)
            info = git.user_repo_info()
            g.user_id.user_repo_info = dumps(info)
            deletions = git.get_deletions()
            g.user_id.deletions = dumps(deletions)

        db_session.commit()

        data.extend([['Repos', len(info[0])],
                ['Forks of user repos', info[1]],
                ['User forked', info[2]]])

        for repo in repo_commits:
            commits.append([repo, repo_commits[repo]])
        total_commits = sum([i[1] for i in commits[1:]])
    return render_template('stats.html', data=data, commits=commits,
                           user=g.user_metadata, total_commits=total_commits,
                           deletions=deletions)


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/user')
def user():
    return str(g.user_metada)
