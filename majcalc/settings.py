import os
from majcalc import app
SECRET_KEY = "2333Helllo"
#SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://' + os.path.join(app.root_path, 'database.db'))
SQLALCHEMY_DATABASE_URI = 'mysql://root:intmainreturn0;@localhost/db'
SQLALCHEMY_TRACK_MODIFICATIONS = False