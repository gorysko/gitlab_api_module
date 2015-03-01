#! /usr/bin/env python
"""Server module, based on flask."""
from json import dumps
from json import loads

from flask import render_template
from flask import g
from flask import url_for
from flask import redirect

from app import app
from app import get_pages_by_type
from app import db_session
from modules import github as git_wrapper


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


@app.route('/user')
def user():
    return str(g.user_metada)
