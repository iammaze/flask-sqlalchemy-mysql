import os
import json
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from serializers import AlchemyEncoder

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# create the DB on demand
@app.before_first_request
def create_tables():
    db.create_all()


class Index(Resource):
    def get(self):
        ret = []
        res = User.query.all()
        for user in res:
            ret.append(
                {
                    'username': user.username,
                    'email': user.email
                }
            )
        return ret, 200


api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
