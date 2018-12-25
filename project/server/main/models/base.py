import datetime
from server.app import db
from server.main.utils import current_datetime

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime(timezone=True))
    modified_at = db.Column(db.DateTime(timezone=True), onupdate=current_datetime())
 
    def __repr__(self):
        return (f"<{self.__class__.__name__}(id={self.id})>")

    def new(self):
        self.created_at = current_datetime()
        self.modified_at = current_datetime()
        db.session.add(self)    
        self.save()

    def update(self, **kwargs):
        raise NotImplementedError

    def delete(self):
        db.session.delete(self)
        self.save()

    def save(self):
        db.session.commit()


    @classmethod
    def get(cls, id):
        return cls.query.filter_by(id=id).first()