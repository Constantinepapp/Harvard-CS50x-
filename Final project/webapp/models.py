from datetime import date
from webapp import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    resting_hr=db.Column(db.Integer,nullable=False)
    max_hr=db.Column(db.Integer,nullable=False)
    lactate_th=db.Column(db.Integer,nullable=False)
    posts=db.relationship('Post',backref="athlete",lazy=True)
    

class Post(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    date=db.Column(db.String(20),nullable=False)
    duration=db.Column(db.Float,nullable=False)
    distance=db.Column(db.Float,nullable=False)
    Heart_rate=db.Column(db.Integer,nullable=False)
    up=db.Column(db.Integer,nullable=False)
    down=db.Column(db.Integer,nullable=False)
    running_index=db.Column(db.Float,nullable=False)
    tss=db.Column(db.Float,nullable=False)
    trimp=db.Column(db.Float)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    
    

    def __repr__(self):
        return "done"
