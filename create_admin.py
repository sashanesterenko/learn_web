from getpass import getpass
import sys

from webapp import create_app
from webapp.model import db, User

app = create_app()

with app.app_context():
    username = input('Fill in username field: ')

    if User.query.filter(User.username == username).count():
        print('Username already exists.')
        sys.exit(0)

    password1 = getpass('Fill in password field: ')
    password2 = getpass('Again: ')

    if not password1 == password2:
        print('Passwords do not match.')
        sys.exit(0)
    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} has been created'.format(new_user.id))