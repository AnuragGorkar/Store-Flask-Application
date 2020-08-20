import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.userResource import UserRegister
from resources.itemResource import Item, ItemList 
from resources.storeResource import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =   os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'anurag'
api = Api(app)


jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__': #This is to run the flask app only when it is executed using python app.py command and not allow it to run when some other programme runs which imports app.py while it is parsing through the imports.
    from db import db
    db.init_app(app)
    app.run(port = 5000, debug = True)