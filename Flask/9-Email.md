### token serializer

```python
import time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


s = Serializer('secret', 5)
token = s.dumps({'user_id': 1}).decode('utf-8')
print(token)

print(s.loads(token))
print('Waiting 10 secs', 'token expiring in 5')
time.sleep(10)
print(s.loads(token))

```



`models.py`

```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
...
class User(db.Model, UserMixin):
	...
    
    def get_reset_token(self, expires_sec=1800):  # 30 minutes
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
```



`forms.py`

```python
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')
                                                 ]
                                     )
    submit = SubmitField('Reset Password')

```



### Reset request

`routes.py`

```python
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm

...
@app.route("/reset_password",  methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template('reset_request.html', title='Reset Password', form=form)

```



`reset_request.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <form class="" action="" method="POST">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Reset Password</legend>
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
        </fieldset>
        <div class="form-group">
          {{ form.submit(class="btn btn-outline-info") }}
        </div>
    </form>
  </div>
{% endblock content %}

```



### reset page

`routes.py`

```python
@app.route("/reset_password/<token>",  methods=['GET', 'POST'])
def reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    return render_template('reset_token.html', title='Reset Password', form=form)
```

`reset_token.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <form class="" action="" method="POST">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Reset Password</legend>
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
{% endblock content %}
```

### validation

```shell
pip install flask-mail
```

`__init__.py`

```python
from flask_mail import Mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'username'  # os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = 'blahblah'
mail = Mail(app)
```



`routes.py`

```python
from flaskblog import app, db, bcrypt, mail
from flask_mail import Message

...
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no change will happen.
'''
    mail.send(msg)


@app.route("/reset_password",  methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>",  methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

```



`login.html`

```html
        <div class="form-group">
          {{ form.submit(class="btn btn-outline-info") }}
          <small class="text-muted ml-2">
            <a href="{{ url_for('reset_request') }}">Forgot Password?</a>
          </small>
        </div>
```

