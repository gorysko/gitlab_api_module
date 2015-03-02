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

from flask_bootstrap import Bootstrap
from flask.ext.assets import Environment
from flask.ext.markdown import Markdown
from flask.ext.flatpages import FlatPages
from flask.ext.flatpages import pygments_style_defs
from flask.ext.github import GitHub

from app.users import users
from modules import github as git_wrapper

from app.config import GITHUB_CLIENT_ID
from app.config import GITHUB_CLIENT_SECRET
from app.config import GITHUB_BASE_URL
from app.config import GITHUB_AUTH_URL
from app.config import SECRET_KEY
from app.database import engine
from app.database import Base
from app.database import db_session

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)

ASSETS = Environment(app)
MARKDOWN = Markdown(app)
PAGES = FlatPages(app)



app.config['GITHUB_CLIENT_ID'] = GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = GITHUB_CLIENT_SECRET

app.config['GITHUB_BASE_URL'] = GITHUB_BASE_URL
app.config['GITHUB_AUTH_URL'] = GITHUB_AUTH_URL


github = GitHub(app)

User = users.User


def init_db():
    """init database."""
    Base.metadata.create_all(engine)


def get_pages_by_type(page_type):
    """Gets page path."""
    page_list = list(PAGES)
    matches = [source for source in page_list \
                if source.meta.get('type') == page_type]
    return matches


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
    return render_template('index.html', user=g.user_metadata)


@app.route('/pygments.css')
def pygments_css():
    """Renders css."""
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}


@app.route('/<path:path>/')
def page(path):
    """Renders page."""
    source = PAGES.get_or_404(path)
    return render_template('page.html', user=g.user_metadata, page=source)


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


@app.route('/login/')
def login():
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


# @app.route('/stats', methods=['GET'])
# def stats():
#     data = [['Type of repos', 'Number of items']]
#     commits = [['Repo name', 'Number of commits']]
#     deletions = []
#     total_commits = 0

#     if g.user_metadata is not None:
#         git = git_wrapper.GithubApi(app.config['GITHUB_BASE_URL'],
#               g.user_metadata['login'], app.config['GITHUB_CLIENT_ID'],
#               app.config['GITHUB_CLIENT_SECRET'])

#         if g.user_id.repo_commits is not None and \
#             g.user_id.user_repo_info is not None and \
#             g.user_id.deletions is not None:

#             repo_commits = loads(g.user_id.repo_commits)
#             info = loads(g.user_id.user_repo_info)
#             deletions = loads(g.user_id.deletions)
#         else:
#             repo_commits = git.commits_by_repo()
#             g.user_id.repo_commits = dumps(repo_commits)
#             info = git.user_repo_info()
#             g.user_id.user_repo_info = dumps(info)
#             deletions = git.get_deletions()
#             g.user_id.deletions = dumps(deletions)

#         db_session.commit()

#         data.extend([['Repos', len(info[0])],
#                 ['Forks of user repos', info[1]],
#                 ['User forked', info[2]]])

#         for repo in repo_commits:
#             commits.append([repo, repo_commits[repo]])
#         total_commits = sum([i[1] for i in commits[1:]])
#     return render_template('stats.html', data=data, commits=commits,
#                            user=g.user_metadata, total_commits=total_commits,
#                            deletions=deletions)

@github.access_token_getter
def token_getter():
    user_data = g.user_id
    if user_data is not None:
        return user_data.github_access_token



@app.route('/logout/')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


from app.users.views import mod as usersModule
app.register_blueprint(usersModule)
