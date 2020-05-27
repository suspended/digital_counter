from passlib.hash import sha256_crypt

from app import db

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def create_super_user(username, password):
        result = User.query.first()
        # make sure only 1 super user is created
        if result is not None:
            return None
        
        password = sha256_crypt.encrypt(password)
        user = User(username, password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return None
        return user

    @staticmethod
    def login_user(username, password):
        result = User.query.filter_by(username=username).first()
        if result is None:
            return None
        if result.username == username and sha256_crypt.verify(password, result.password):
            return result
        else:
            return None
        