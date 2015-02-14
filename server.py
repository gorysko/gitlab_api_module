#! /usr/bin/env python
"""Server module, based on flask."""

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import g
from flask import url_for
from flask import redirect
from flask.ext.github import GitHub

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

app.config['DATABASE_URI'] = 'sqlite:////tmp/github.db'

app.config['GITHUB_CLIENT_ID'] = '5a80a178d27e64a4d264'
app.config['GITHUB_CLIENT_SECRET'] = '243aa848374960e115494977cada492466f47902'

app.config['GITHUB_BASE_URL'] = 'https://api.github.com/'
app.config['GITHUB_AUTH_URL'] = 'https://github.com/login/oauth/'


github = GitHub(app)

engine = create_engine(app.config['DATABASE_URI'])
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """init database."""
    Base.metadata.create_all(bind=engine)


class User(Base):
    """User class."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    github_access_token = Column(String(200))

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
    data = []
    user = {}
    if g.user_metadata is not None:
        git = git_wrapper.GithubApi(app.config['GITHUB_BASE_URL'],
              g.user_metadata['login'])
        data = [('Repos', len(git.get_user_repos())),
                ('Repos Watched', len(git.get_user_repos_watched())),
                ('Gists', len(git.get_user_gists()))]
    return render_template('first.html', data=data, user=g.user_metadata)


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


def _init_api(user_name, api_url, git=True):
    if git:
        if api_url is None:
            api_url = app.config['GITHUB_BASE_URL']
        api = git_wapper.GithubApi(api_url, user_name)
        return api
    return None


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
