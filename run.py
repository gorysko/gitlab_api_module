#! /usr/bin/env python

"""Running the application."""
from app import app
from app import init_db

init_db()

app.run(debug=True)
