
from server.app import db
from server.main.utils import current_datetime

class BlacklistedTokenModel(db.Model):

    __tablename__ = "blacklisted_tokens"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    blackisted_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return (f"<{self.__class__.__name__}(token={self.token})>")

    @classmethod
    def get(cls, token):
        return cls.query.filter_by(token=token).first()

    def save(self):
        self.blackisted_at = current_datetime()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check(token):
        result = BlacklistedTokenModel.get(token)
        if result:
            return True
        return False