#! /usr/bin/env python
"""Server module, based on flask."""

from flask import Flask
from flask import render_template
from flask import request
from flask_bootstrap import Bootstrap

from application import github

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET'])
def hello_world(name=None):
    return render_template('first.html', name=name)


@app.route('/stats', methods=['GET', 'POST'])
def get():
    user = request.args.get('user', '')
    repo = request.args.get('repo_name', '')
    api = _init_api(user)
    return render_template('stats.html', user=user, repo=repo,
                           languages=api.get_repo_info(repo, 'languages'),
                           branches=api.get_repo_info(repo, 'branches'),
                           contributors=api.get_repo_info(repo, 'contributors'))


def _init_api(user_name, git=True):
    if git:
        api = github.GithubApi('https://api.github.com/', user_name)
        return api
    return None

if __name__ == '__main__':
    app.run(debug=True)