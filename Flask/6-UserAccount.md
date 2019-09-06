`account.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <div class="media">
      <img class="rounded-circle account-img" src={{ image_file }}>
      <div class="media-body">
        <h2 class="account-heading">{{ current_user.username }}</h2>
        <p class="text-secondary">{{ current_user.email }}</p>
      </div>
    </div>
    <!-- FORM HERE -->
  </div>
{% endblock content %}

```

static/profile_pics/default.jpg

`routes.py`

```python
@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account', image_file=image_file, form=form)

```

`forms.py`

```python
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]
                           )
    email = StringField('Email', validators=[DataRequired(), Email()])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

```

`account.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <div class="media">
      <img class="rounded-circle account-img" src={{ image_file }}>
      <div class="media-body">
        <h2 class="account-heading">{{ current_user.username }}</h2>
        <p class="text-secondary">{{ current_user.email }}</p>
      </div>
    </div>
    <form class="" action="" method="POST">
        {{ form.hidden_tag() }}
        <fieldset class="form-group">
          <legend class="border-bottom mb-4">Account Info</legend>
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
        </fieldset>
        <div class="form-group">
          {{ form.submit(class="btn btn-outline-info") }}
        </div>
    </form>
  </div>
{% endblock content %}

```



### Image

`forms.py`

```python
from flask_wtf.file import FileField, FileAllowed
...
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)]
                           )
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
```



`account.html`   + encoding

```html

    <form class="" action="" method="POST" enctype="multipart/form-data">
        ...
		<div class="form-group">
            {{ form.picture.label() }}
            {{ form.picture(class="form-control-file")}}
            {% if form.picture.errors %}
              {% for error in form.picture.errors %}
                <span class="text-danger">{{ error }}</span><br>
              {% endfor %}
            {% endif %}
          </div>
```

`routes.py`

```python

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route("/account",  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html',
                           title='Account', image_file=image_file, form=form)

```



### resize images

using pillow

```shell
pip install Pillow
```

`routes.py`

```python
from PIL import Image

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    
    i.save(picture_path)
    return picture_fn
```

