templates/home.html

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <h1>Home Page!</h1>
  </body>
</html>

```

flaskblog.py

```python
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)

```



templates/layout.html

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    {% if title %}
      <title>Flask Blog - {{ title }}</title>
    {% else %}
      <title>Flask Blog</title>
    {% endif %}
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>

```

templates/home.html

```html
{% extends "layout.html" %}
{% block content %}
    <h1>Home Page!</h1>
    {% for post in posts %}
      <h1>{{ post.title }}</h1>
      <p>By {{ post.author }} on {{ post.date_posted }}</p>
      <p>{{ post.content }}</p>
    {% endfor%}
{% endblock content %}

```

templates/about.html

```html
{% extends "layout.html" %}
{% block content %}
  <h1>About Page!</h1>
{% endblock content %}

```



# Using Bootstrap

https://getbootstrap.com/docs/4.0/getting-started/introduction/

```html
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>
```



layout.html

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    {% if title %}
      <title>Flask Blog - {{ title }}</title>
    {% else %}
      <title>Flask Blog</title>
    {% endif %}
  </head>
  <body>
    <div class="container">
      {% block content %}{% endblock %}      
    </div>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
  </body>
</html>

```



# Navigation Bar

https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/navigation.html

```html
<header class="site-header">
  <nav class="navbar navbar-expand-md navbar-dark bg-steel fixed-top">
    <div class="container">
      <a class="navbar-brand mr-4" href="/">Flask Blog</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarToggle">
        <div class="navbar-nav mr-auto">
          <a class="nav-item nav-link" href="/">Home</a>
          <a class="nav-item nav-link" href="/about">About</a>
        </div>
        <!-- Navbar Right Side -->
        <div class="navbar-nav">
          <a class="nav-item nav-link" href="/login">Login</a>
          <a class="nav-item nav-link" href="/register">Register</a>
        </div>
      </div>
    </div>
  </nav>
</header>
```

https://github.com/CoreyMSchafer/code_snippets/blob/master/Django_Blog/snippets/main.html

```html

<main role="main" class="container">
  <div class="row">
    <div class="col-md-8">
      {% block content %}{% endblock %}
    </div>
    <div class="col-md-4">
      <div class="content-section">
        <h3>Our Sidebar</h3>
        <p class='text-muted'>You can put any information here you'd like.
          <ul class="list-group">
            <li class="list-group-item list-group-item-light">Latest Posts</li>
            <li class="list-group-item list-group-item-light">Announcements</li>
            <li class="list-group-item list-group-item-light">Calendars</li>
            <li class="list-group-item list-group-item-light">etc</li>
          </ul>
        </p>
      </div>
    </div>
  </div>
</main>
```



```shell
touch /static/main.css
```

```css
body {
  background: #fafafa;
  color: #333333;
  margin-top: 5rem;
}

h1, h2, h3, h4, h5, h6 {
  color: #444444;
}

ul {
  margin: 0;
}

.bg-steel {
  background-color: #5f788a;
}

.site-header .navbar-nav .nav-link {
  color: #cbd5db;
}

.site-header .navbar-nav .nav-link:hover {
  color: #ffffff;
}

.site-header .navbar-nav .nav-link.active {
  font-weight: 500;
}

.content-section {
  background: #ffffff;
  padding: 10px 20px;
  border: 1px solid #dddddd;
  border-radius: 3px;
  margin-bottom: 20px;
}

.article-title {
  color: #444444;
}

a.article-title:hover {
  color: #428bca;
  text-decoration: none;
}

.article-content {
  white-space: pre-line;
}

.article-img {
  height: 65px;
  width: 65px;
  margin-right: 16px;
}

.article-metadata {
  padding-bottom: 1px;
  margin-bottom: 4px;
  border-bottom: 1px solid #e3e3e3
}

.article-metadata a:hover {
  color: #333;
  text-decoration: none;
}

.article-svg {
  width: 25px;
  height: 25px;
  vertical-align: middle;
}

.account-img {
  height: 125px;
  width: 125px;
  margin-right: 20px;
  margin-bottom: 16px;
}

.account-heading {
  font-size: 2.5rem;
}
```

in base.html - load the css

```html
{% load static %}
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

      <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css')}}">
```

flaskblog.py

```python
from flask import Flask, render_template, url_for
app = Flask(__name__)
```



### More Styling

from article.html -> for loop in home.html

```html
<article class="media content-section">
  <div class="media-body">
    <div class="article-metadata">
      <a class="mr-2" href="#">{{ post.author }}</a>
      <small class="text-muted">{{ post.date_posted }}</small>
    </div>
    <h2><a class="article-title" href="#">{{ post.title }}</a></h2>
    <p class="article-content">{{ post.content }}</p>
  </div>
</article>
```



