import json
from flaskblog import db
from flaskblog.models import Post


with open('posts.json') as json_file:
    posts = json.load(json_file)

print(f'Number of posts to add -> {len(posts)}')

db.create_all()
print(f'Number of posts before adding -> {len(Post.query.all())}')
for post in posts:
    p = Post(title=post.get('title'), content=post.get('content'), user_id=post.get('user_id'))
    db.session.add(p)
db.session.commit()
print(f'Number of posts after adding -> {len(Post.query.all())}')
