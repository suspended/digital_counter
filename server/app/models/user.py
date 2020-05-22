from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def create_user(username, password):
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
        if result.username == username and result.password == password:
            return result
        else:
            return None
        