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
from app.users.views import mod as usersModule

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

app.register_blueprint(usersModule)


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
    """before request action"""
    g.user_id = None
    g.user_metadata = None
    if 'user_id' in session:
        g.user_id = User.query.get(session['user_id'])
        g.user_metadata = github.get('user')


@app.after_request
def after_request(response):
    """after request action"""
    db_session.remove()
    return response


@app.route('/', methods=['GET'])
def index(name=None):
    """index view of application."""
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
    """github callback processing for auth."""
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
    """login action."""
    if session.get('user_id', None) is None:
        return github.authorize()
    else:
        return 'Already logged in'


@github.access_token_getter
def token_getter():
    """gets token."""
    user_data = g.user_id
    if user_data is not None:
        return user_data.github_access_token



@app.route('/logout/')
def logout():
    """logout action."""
    session.pop('user_id', None)
    return redirect(url_for('index'))
