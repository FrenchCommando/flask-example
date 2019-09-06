```shell
pip install flask-sqlalchemy
```



flaskblog.py

```python
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '62adc56596a2b79d36976446d18308b7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

```

```python
Python 3.7.3 (default, Apr  3 2019, 05:39:12) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from flaskblog import db
/home/frenchcommando/Projects/flask/venv/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:835: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
>>> db.create_all()
>>> from flaskblog import User, Post
>>> user_1 = User(username='Corey', email='C@demo.com', password='password')
>>> db.session.add(user_1)
>>> user_2 = User(username='JohnDoe', email='jd@demo.com', password='password')
>>> db.session.add(user_2)
>>> db.session.commit()
>>> User.query.all()
[User('Corey', 'C@demo.com', 'default.jpg'), User('JohnDoe', 'jd@demo.com', 'default.jpg')]
>>> User.query.first()
User('Corey', 'C@demo.com', 'default.jpg')
>>> User.query.filter_by(username='Corey').all()
[User('Corey', 'C@demo.com', 'default.jpg')]
>>> User.query.filter_by(username='Corey').first
<bound method Query.first of <flask_sqlalchemy.BaseQuery object at 0x7f1a698d4550>>
>>> User.query.filter_by(username='Corey').first()
User('Corey', 'C@demo.com', 'default.jpg')
>>> user = User.query.filter_by(username='Corey').first()
>>> user
User('Corey', 'C@demo.com', 'default.jpg')
>>> user.id
1
>>> user= User.query.get(1)
>>> user
User('Corey', 'C@demo.com', 'default.jpg')
>>> user.posts
[]
>>> post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)
>>> post_1
Post('Blog 1', 'None')
>>> post_2 = Post(title='Blog 2', content='Second Post Content!', user_id=user.id)
>>> db.session.add(post_1)
>>> db.session.add(post_2)
>>> db.session.commit()
>>> user.posts
[Post('Blog 1', '2019-09-05 04:24:51.001409'), Post('Blog 2', '2019-09-05 04:24:51.002055')]
>>> for post in user.posts:
...     print(post.title)
... 
Blog 1
Blog 2
>>> post = Post.query.first()
>>> post
Post('Blog 1', '2019-09-05 04:24:51.001409')
>>> post.user_id
1
>>> post.author
User('Corey', 'C@demo.com', 'default.jpg')
>>> 
>>> 
>>> db.drop_all()
>>> 
>>> db.create_all()
>>> User.query.all()
[]
>>> Post.query.all()
[]
>>> 

```

