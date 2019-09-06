### Generate secret key

```python
import secrets
secrets.token_hex(16)
```







### Install wtf

```shell
pip install wtf
pip install flask-wtf
```

## Forms

flaskblog.py

```python
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)


app.config['SECRET_KEY'] = '62adc56596a2b79d36976446d18308b7'

...

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)
```



forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]
                           )
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')
                                                 ]
                                     )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

```



register.html

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <form class="" action="" method="POST">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Join Today</legend>
          <div class="form-group">
            {{ form.username.label(class="form-control-label") }}

            {% if form.username.errors %}
              {{ form.username(class="form-control form-control-lg is-invalid") }}
              <div class="invalid-feedback">
                {% for error in form.username.errors %}
                  <span>{{ error }}</span>
                {% endfor %}
              </div>
            {% else %}
              {{ form.username(class="form-control form-control-lg") }}
            {% endif %}
          </div>
          <div class="form-group">
            {{ form.email.label(class="form-control-label") }}
            {% if form.email.errors %}
              {{ form.email(class="form-control form-control-lg is-invalid") }}
              <div class="invalid-feedback">
                {% for error in form.email.errors %}
                  <span>{{ error }}</span>
                {% endfor %}
              </div>
            {% else %}
              {{ form.email(class="form-control form-control-lg") }}
            {% endif %}
          </div>
          <div class="form-group">
            {{ form.password.label(class="form-control-label") }}
            {% if form.password.errors %}
              {{ form.password(class="form-control form-control-lg is-invalid") }}
              <div class="invalid-feedback">
                {% for error in form.password.errors %}
                  <span>{{ error }}</span>
                {% endfor %}
              </div>
            {% else %}
              {{ form.password(class="form-control form-control-lg") }}
            {% endif %}
          </div>
          <div class="form-group">
            {{ form.confirm_password.label(class="form-control-label") }}
            {% if form.confirm_password.errors %}
              {{ form.confirm_password(class="form-control form-control-lg is-invalid") }}
              <div class="invalid-feedback">
                {% for error in form.confirm_password.errors %}
                  <span>{{ error }}</span>
                {% endfor %}
              </div>
            {% else %}
              {{ form.confirm_password(class="form-control form-control-lg") }}
            {% endif %}
          </div>
        </fieldset>
        <div class="form-group">
          {{ form.submit(class="btn btn-outline-info") }}
        </div>
    </form>
  </div>
  <div class="border-top pt-3">
    <small class="text-muted">
      Already have an account ? <a class="ml-2" href="{{ url_for('login') }}">Sign In</a>
    </small>
  </div>
{% endblock content %}

```



### Display flash content

layout.html

```html
                    <div class="navbar-nav mr-auto">
              <a class="nav-item nav-link" href="{{ url_for('home')}}">Home</a>
              <a class="nav-item nav-link" href="{{ url_for('about')}}">About</a>
            </div>
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              <a class="nav-item nav-link" href="{{ url_for('login')}}">Login</a>
              <a class="nav-item nav-link" href="{{ url_for('register')}}">Register</a>
            </div>

...
{% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
              {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                  {{ message }}
                </div>
              {% endfor %}
            {% endif %}
          {% endwith %}
          {% block content %}{% endblock %}
```



login.html

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <form class="" action="" method="POST">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Log In</legend>
          <div class="form-group">
            {{ form.email.label(class="form-control-label") }}
            {% if form.email.errors %}
              {{ form.email(class="form-control form-control-lg is-invalid") }}
              <div class="invalid-feedback">
                {% for error in form.email.errors %}
                  <span>{{ error }}</span>
                {% endfor %}
              </div>
            {% else %}
              {{ form.email(class="form-control form-control-lg") }}
            {% endif %}
          </div>
          <div class="form-group">
            {{ form.password.label(class="form-control-label") }}
            {% if form.password.errors %}
              {{ form.password(class="form-control form-control-lg is-invalid") }}
              <div class="invalid-feedback">
                {% for error in form.password.errors %}
                  <span>{{ error }}</span>
                {% endfor %}
              </div>
            {% else %}
              {{ form.password(class="form-control form-control-lg") }}
            {% endif %}
          </div>
          <div class="form-check">
            {{ form.remember(class="form-check-input")}}
            {{ form.remember.label(class="form-check-label")}}
          </div>
        </fieldset>
        <div class="form-group">
          {{ form.submit(class="btn btn-outline-info") }}
        </div>
        <small class="text-muted ml-2">
          <a href="#">Forgot Password?</a>
        </small>
    </form>
  </div>
  <div class="border-top pt-3">
    <small class="text-muted">
      Need an account ? <a class="ml-2" href="{{ url_for('register') }}">Sign Up Now</a>
    </small>
  </div>
{% endblock content %}

```

