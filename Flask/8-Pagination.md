## push new posts

`import_posts_from_json.py`

```python
import json
from flaskblog import db
from flaskblog.models import Post


with open('posts.json') as json_file:
    posts = json.load(json_file)

print(f'Number of posts {len(posts)}')

db.create_all()
for post in posts:
    p = Post(title=post.get('title'), content=post.get('content'), user_id=post.get('user_id'))
    db.session.add(p)
db.session.commit()
```



### Pagination

`routes.py`

```python
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)
```

`home.html`

```html
    {% for post in posts.items %}
```

http://127.0.0.1:5000/home?page=2



### links

`home.html`

```html
    {% endfor%}
    {% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2) %}
      {% if page_num %}
        {% if posts.page == page_num %}
          <a class="btn btn-info mb-4" href="{{ url_for('home', page=page_num) }}">{{ page_num }}</a>
        {% else %}
          <a class="btn btn-outline-info mb-4" href="{{ url_for('home', page=page_num) }}">{{ page_num }}</a>
        {% endif %}
      {% else %}
        ...
      {% endif %}
    {% endfor %}
{% endblock content %}
```

### posts orders

`routes.py`

```python
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
```



## User specific posts

`routes.py`

```python
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

```



'user_posts.html'

```html
{% extends "layout.html" %}
{% block content %}
  <h1 class="mb-3">Posts by {{ user.username }} ({{ posts.total }})</h1>
    {% for post in posts.items %}
      <article class="media content-section">
        <img class="rounded-circle article-img" src="{{ url_for('static', filename='profile_pics/' + post.author.image_file) }}" alt="">
        <div class="media-body">
          <div class="article-metadata">
            <a class="mr-2" href="{{ url_for('user_posts', username=post.author.username) }}">{{ post.author.username }}</a>
            <small class="text-muted">{{ post.date_posted.strftime('%Y-%m-%d') }}</small>
          </div>
          <h2><a class="article-title" href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
          <p class="article-content">{{ post.content }}</p>
        </div>
      </article>
    {% endfor%}
    {% for page_num in posts.iter_pages(left_edge=1, right_edge=1, left_current=3, right_current=4) %}
      {% if page_num %}
        {% if posts.page == page_num %}
          <a class="btn btn-info mb-4" href="{{ url_for(user_posts', username=user.username, page=page_num) }}">{{ page_num }}</a>
        {% else %}
          <a class="btn btn-outline-info mb-4" href="{{ url_for(user_posts', username=user.username, page=page_num) }}">{{ page_num }}</a>
        {% endif %}
      {% else %}
        ...
      {% endif %}
    {% endfor %}
{% endblock content %}

```

`home.html`

```html
            <a class="mr-2" href="{{ url_for('user_posts', username=post.author.username) }}">{{ post.author.username }}</a>

```

