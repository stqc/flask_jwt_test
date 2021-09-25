from backend import db

class users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(30))

    def __init__(self,uname,pword):
        self.username = uname
        self.password = pword