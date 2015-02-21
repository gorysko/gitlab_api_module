#! /usr/bin/env python
"""Server module, based on flask."""
import os

from json import dumps
from json import loads

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import g
from flask import url_for
from flask import redirect
from flask.ext.github import GitHub
from flask.ext.sqlalchemy import SQLAlchemy

from application import github as git_wrapper

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SECRET_KEY = 'development key'
DEBUG = True

GITHUB_CLIENT_ID = '5a80a178d27e64a4d264'
GITHUB_CLIENT_SECRET = '243aa848374960e115494977cada492466f47902s'


app = Flask(__name__)
app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///github.db'


# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

app.config['GITHUB_CLIENT_ID'] = '5a80a178d27e64a4d264'
app.config['GITHUB_CLIENT_SECRET'] = '243aa848374960e115494977cada492466f47902'

app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'


github = GitHub(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """init database."""
    Base.metadata.create_all(engine)


class User(Base):
    """User class."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    github_access_token = Column(String)
    user_repo_info = Column(String)
    repo_commits = Column(String)
    deletions = Column(String)


    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

@app.before_request
def before_request():
    g.user_id = None
    g.user_metadata = None
    if 'user_id' in session:
        g.user_id = User.query.get(session['user_id'])
        g.user_metadata = github.get('user')

@app.after_request
def after_request(response):
    db_session.remove()
    return response

@app.route('/', methods=['GET'])
def index(name=None):
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
    return render_template('first.html', data=data, commits=commits,
                           user=g.user_metadata, total_commits=total_commits,
                           deletions=deletions)


@github.access_token_getter
def token_getter():
    user = g.user_id
    if user is not None:
        return user.github_access_token


@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)
    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db_session.add(user)
    user.github_access_token = access_token
    db_session.commit()

    session['user_id'] = user.id
    return redirect(url_for('index'))


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


if __name__ == '__main__':
    init_db()
    app.run()
