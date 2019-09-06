`routes.py`

```python
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
...

@app.route("/post/new",  methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',
                           title='New Post',
                           form=form
                           )

```

`create_post.html`

```html
{% extends "layout.html" %}
{% block content %}
<div class="content-section">
  <form class="" action="" method="POST">
    {{ form.hidden_tag() }}
    <fieldset class="form-group">
      <legend class="border-bottom mb-4">New Post</legend>
      <div class="form-group">
        {{ form.title.label(class="form-control-label") }}
        {% if form.title.errors %}
          {{ form.title(class="form-control form-control-lg is-invalid") }}
          <div class="invalid-feedback">
            {% for error in form.title.errors %}
              <span>{{ error }}</span>
            {% endfor %}
          </div>
        {% else %}
          {{ form.title(class="form-control form-control-lg") }}
        {% endif %}
      </div>
      <div class="form-group">
        {{ form.content.label(class="form-control-label") }}
        {% if form.content.errors %}
          {{ form.content(class="form-control form-control-lg is-invalid") }}
          <div class="invalid-feedback">
            {% for error in form.content.errors %}
              <span>{{ error }}</span>
            {% endfor %}
          </div>
        {% else %}
          {{ form.content(class="form-control form-control-lg") }}
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

`forms.py`

```python
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
...
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

```

`layout.html`

```html
                <a class="nav-item nav-link" href="{{ url_for('new_post')}}">New Post</a>
                <a class="nav-item nav-link" href="{{ url_for('account')}}">Account</a>
                <a class="nav-item nav-link" href="{{ url_for('logout')}}">Logout</a>
```



## Adding to database

`routes.py`

```python
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route("/post/new",  methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',
                           title='New Post',
                           form=form
                           )

```



### Display Post styles

`home.html`

```html
      <article class="media content-section">
        <img class="rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.author.image_file) }}" alt="">
        <div class="media-body">
          <div class="article-metadata">
            <a class="mr-2" href="#">{{ post.author.username }}</a>
            <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
          </div>
```

### ID of Posts

`routes.py`

```python

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

```

`post.html`

```html
{% extends "layout.html" %}
{% block content %}
  <article class="media content-section">
    <img class="rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.author.image_file) }}" alt="">
    <div class="media-body">
      <div class="article-metadata">
        <a class="mr-2" href="#">{{ post.author.username }}</a>
        <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
      </div>
      <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
      <p class="article-content">{{ post.content }}</p>
    </div>
  </article>
{% endblock content %}
```

`home.html`

```html
          <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
```

### Update Post

`routes.py`

```python
from flask import render_template, url_for, flash, redirect, request, abort
...
@app.route("/post/<int:post_id>/update",  methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',
                           title='Update Post', form=form,
                           legend='Update Post'
                           )

```

`create_post.html`

```html

      <legend class="border-bottom mb-4">{{ legend }}</legend>
```



### Adding links to update

https://getbootstrap.com/docs/4.0/components/modal/

```html
<!-- Button trigger modal -->
<button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
  Launch demo modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
```

`post.html`

```html
{% extends "layout.html" %}
{% block content %}
  <article class="media content-section">
    <img class="rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.author.image_file) }}" alt="">
    <div class="media-body">
      <div class="article-metadata">
        <a class="mr-2" href="#">{{ post.author.username }}</a>
        <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
        {% if post.author == current_user %}
          <div>
            <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{{ url_for('update_post', post_id=post.id)}}">Update</a>
            <button type="button" class="btn btn-danger btn-sm m-1" data-toggle="modal" data-target="#deleteModal">Delete</button>
          </div>
        {% endif %}
      </div>
      <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
      <p class="article-content">{{ post.content }}</p>
    </div>
  </article>

  <!-- Modal -->
<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="deleteModalLabel">Delete Post ?</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <form class="" action="{{ url_for('delete_post', post_id=post.id) }}" method="POST">
          <input type="submit" name="" value="Delete" class="btn btn-danger">
        </form>
        <!-- <button type="button" class="btn btn-primary">Confirm Delete</button> -->
      </div>
    </div>
  </div>
</div>
{% endblock content %}

```

`routes.py`

```python


@app.route("/post/<int:post_id>/delete",  methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # forbidden route
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

```

