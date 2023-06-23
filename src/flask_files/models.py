from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, username, email, password_hash, intolerances):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.intolerances = intolerances

    def get_id(self):
        return self.username

    def get_dict(self):
        return {"username":self.username, "email":self.email, "password":self.password_hash}

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'')"