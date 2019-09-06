```shell
pip install flask
```

flaskblog.py

```python
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Hello World!</h1>"

```

```shell
export FLASK_APP=flaskblog.py
flask run
```

debug - updates changes without having to kill the console

```shell
export FLASK_DEBUG=1
```



to run directly

```python
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "<h1>Hello World! HomePage</h1>"


if __name__ == '__main__':
    app.run(debug=True)

```

```shell
python flaskblog.py
```





### About page

```python
from flask import Flask
app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return "<h1>Hello World! HomePage</h1>"


@app.route("/about")
def about():
    return "<h1>About Page!</h1>"


if __name__ == '__main__':
    app.run(debug=True)

```

