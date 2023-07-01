from core import app, db
from users.model import User
from properties.model import Property, Image
from sys import argv
    
try:
    if argv[1] == 'create':
        with app.app_context():
            db.create_all()
            print('Database(s) created')
    elif argv[1] == 'drop':
        with app.app_context():
            db.drop_all()
            print('Database(s) dropped')
    elif argv[1] == 'refresh':
        with app.app_context():
            db.drop_all()
            db.create_all()
            print('Database(s) refreshed')
    else:
        print(f"ERROR!!! {argv[1]} is an invalid input")
except IndexError:
    print('ERROR!!! Pass an input (create|drop|refresh)')
except Exception as e:
    print(e)