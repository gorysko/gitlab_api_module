"""Users model"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app import database

class User(database.Base):
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