Blueprints



make user / posts / main folders

with `__init__.py`, `forms.py`, `routes.py`, `utils.py`

and move the proper functions



from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email


users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])



replace all the url_for with corresponding blueprint





## Environ variables

```shell
subl ~/.bash_profile
```





`__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app

```



`config.py`  -> he is using environ variable - i am not

```python
import json


with open("/etc/django_config.json") as config_file:
	config = json.load(config_file)

class Config:

    SECRET_KEY = '62adc56596a2b79d36976446d18308b7'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config["EMAIL_USER"]  # os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = config["EMAIL_PASS"]

```







replace app with current_app

```python
from flask import current_app
```

