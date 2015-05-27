"""Users model"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database import Base
from app.database import db_session

class User(Base):
    """User class."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    login = Column(String)
    github_access_token = Column(String)
    user_repo_info = Column(String)
    repo_commits = Column(String)
    deletions = Column(String)
    contrib_repo_commits = Column(String)


    def __init__(self, github_access_token):
        self.github_access_token = github_access_token
        # self.username = username
        # self.login = login

    @staticmethod
    def get_or_create(login, token):
        user = User.query.filter_by(login=login).first()
        if user is None:
            user = User(token)
            db_session.add(user)
            db_session.commit()
        return user