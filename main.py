from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.views import MethodView
import datetime
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI ='postgresql+Psycopg 2://admin:1234@127.0.0.1:5431/my_db')

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

class Views(MethodView):
    def post(self):
        adv = Advertisement(**request.json)
        adv.add()
        return jsonify(adv.to_dict())

    def delete(self, adv_id):
        adv = Advertisement(**request.json)
        db.session.delete(adv.by_id(adv_id))
        return db.session.commit()


app.add_url_rule('/advertisment/post', view_func= Views.as_view('post_adv'), methods=['POST', ])
app.add_url_rule('/delete', view_func= Views.as_view('remove adv'), methods=['DELETE', ])

app.run()
