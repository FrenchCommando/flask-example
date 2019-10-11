from flaskblog import db, create_app
from flaskblog.models import User


with create_app().app_context():
	db.create_all()

	for i in range(10):
		user = User(username='name' + str(i), email='C{}@demo.com'.format(str(i)), password='password')
		db.session.add(user)

	print(f'Number of users before adding -> {len(User.query.all())}')
	db.session.commit()
	print(f'Number of users after adding -> {len(User.query.all())}')