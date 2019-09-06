`errors/handlers.py`

```python
from flask import Blueprint, render_template


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500

```

`errors/403.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <h1>You don't have permission to do that (403)</h1>
    <p>Please check your account and try again.</p>
  </div>
{% endblock content %}

```

`errors/404.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <h1>Oops. Page Not Found (404)</h1>
    <p>That page does not exist. Please try a different location.</p>
  </div>
{% endblock content %}

```

`errors/500.html`

```html
{% extends "layout.html" %}
{% block content %}
  <div class="content-section">
    <h1>Something went wrong (500)</h1>
    <p>We are experiencing some trouble on our end. Please try again in the future.</p>
  </div>
{% endblock content %}

```

