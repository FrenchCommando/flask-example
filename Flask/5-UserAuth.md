Debug with PIN -> run python console



### decrypt

```shell
pip install flask-bcrypt
```

```python
>>> from flask_bcrypt import Bcrypt
>>> bcrypt = Bcrypt()
>>> bcrypt.generate_password_hash('testing')
b'$2b$12$fCYhaJXRM5xZXXAkore/D.xecCE6QSoKQG8BCfbtBV.Z98eUfaPme'
>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$CtDsS.dmJMb88xuX5ZjnKOX8HwEQPgMvLwwMlwWlb9xYTabj/GFRW'
>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$KDDDjfbcwapaT0M6TPmepeYac52i33xL1zZu1Y7zc0XkbHqjTwiJW'
>>> bcrypt.generate_password_hash('testing').decode('utf-8')
'$2b$12$TIZkMiFUYix8NgcVhNRriezj6eTqjKPGiNaL17KsqfVy7iMYEt.8i'
>>> hashed_pw = bcrypt.generate_password_hash('testing').decode('utf-8')
>>> bcrypt.check_password_hash(hashed_pw, 'password')
False
>>> bcrypt.check_password_hash(hashed_pw, 'testing')
True
```



`__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = '62adc56596a2b79d36976446d18308b7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
```



`routes.py`

```python
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in!', 'success')
        # f'Account created for {form.username.data}!'
```

`forms.py`

```python
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')
```



### Login

```python
pip install flask-login
```

`__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '62adc56596a2b79d36976446d18308b7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
```



`models.py`

```python
from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
```

`routes.py`

```python
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
...
    
    
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
    
```



### logout

`routes.py`

```python
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

```



`layout.html`

```html
            <div class="navbar-nav">
              {% if current_user.is_authenticated %}
                <a class="nav-item nav-link" href="{{ url_for('logout')}}">Logout</a>
              {% else %}
                <a class="nav-item nav-link" href="{{ url_for('login')}}">Login</a>
                <a class="nav-item nav-link" href="{{ url_for('register')}}">Register</a>
              {% endif%}
            </div>
```



### account required

`routes.py` - requires to be logged in

```python
@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

```

`account.html`

```html
{% extends "layout.html" %}
{% block content %}
  <h1>{{ current_user.username }}</h1>
{% endblock content %}

```

`layout.html`

```html
              {% if current_user.is_authenticated %}
                <a class="nav-item nav-link" href="{{ url_for('account')}}">Account</a>
                <a class="nav-item nav-link" href="{{ url_for('logout')}}">Logout</a>
              {% else %}
                <a class="nav-item nav-link" href="{{ url_for('login')}}">Login</a>
                <a class="nav-item nav-link" href="{{ url_for('register')}}">Register</a>
              {% endif%}
```



redirect to login

```python
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
```



next page 

`routes.py`

```python
@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login Successful!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
```

