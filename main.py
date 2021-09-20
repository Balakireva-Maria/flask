from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
import datetime


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI = URI)
SALT='AbCd514234#&0)>/6v'

class Exeptions(Exception):
    status_code = 0
    status_message = 'Unknown'

    def __init__(self, message: str = None, status_code: int = None):
        self.message = message
        request.status_code = self.status_code
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'message': self.message or self.status_message}
class NotFound(Exeptions):
    status_code = 404
    status_message = 'Not Found'
class ValidationError(Exeptions):
    status_code = 401
    status_message = 'Auth error'
class BadLuck(Exeptions):
    status_code = 400
    status_message = 'Validation error'

@app.errorhandler(NotFound)
@app.errorhandler(ValidationError)
@app.errorhandler(BadLuck)
def handle_invalid_inquiry(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

class BaseModel:
    @classmethod
    def by_id(cls, id):
        obj = cls.query.get(id)
        if obj:
            return obj
        else:
            raise NotFound

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except:
            raise BadLuck



class User(db.Model, db.BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    email = db.Column(db.String(90), index=True)
    password = db.Column(db.String(90), index=True)

    def __str__(self):
        return 'User '.format(self.username)

    def set_password(self, password: str):
        raw_password = f'{password}{SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{password}{SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.username,
            'email': self.email
        }

class UserView(MethodView):

    def get(self, user_id):
        user = User.by_id(user_id)
        return user.to_dict()

    def post(self):
        user = User(**request.json['password'])
        user.set_password(request.json['password'])
        user.add()
        return user.to_dict()


class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(20), index=True)
    description = db.Column(db.String(600), index=True)
    creation_date = db.Column(db.String, index=True)
    owner = header = db.Column(db.String(20), index=True)

    def add(self):
        db.session.add(self)
        return db.session.commit()


    def by_id(cls, obj_id):
        obj = cls.query.get(obj_id)
        return obj

    def to_dict(self):
        return {'id': self.id, 'header': self.header, 'description': self.description, 'creation_date': datetime.date, 'owner': self.owner }

class AdvViews(MethodView):
    def post(self):
        adv = Advertisement(**request.json)
        adv.add()
        return jsonify(adv.to_dict())

    def delete(self, adv_id):
        adv = Advertisement(**request.json)
        db.session.delete(adv.by_id(adv_id))
        return db.session.commit()


app.add_url_rule('/advertisment/post', view_func= AdvViews.as_view('post_adv'), methods=['POST', ])
app.add_url_rule('/delete', view_func= AdvViews.as_view('remove adv'), methods=['DELETE', ])

app.run()
