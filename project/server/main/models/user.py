
from server.app import db
from server.main.models import BaseModel

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash

class Permission:
    READ = 0
    WRITE = 1
    DELETE = 2
    GENERAL = 254
    ADMINISTRATOR = 255

class RoleModel(db.Model):

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    permission = db.Column(db.Integer, default=Permission.GENERAL)
    users = db.relationship("UserModel", backref="role", lazy=True)

    def __repr__(self):
        return '<Role \'%s\'>' % self.name


    @classmethod
    def get_default(cls):
        return cls.query.filter_by(permission=Permission.GENERAL).first()

    @staticmethod
    def insert():
        roles = {
            "User": [Permission.GENERAL],
            "Administrator": [Permission.ADMINISTRATOR]
        }

        for r in roles:
            role = RoleModel.query.filter_by(name=r).first()

            if not role:
                role = RoleModel(name=r)
            role.permission = roles[r][0]
            db.session.add(role)
        db.session.commit()

class GroupModel(db.Model):
    __modelname__ = "Group"

    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))

    @property
    def leader(self):
        return GroupModel.query.filter(GroupModel.members.has(is_lead=True)).first()

class GroupMemberModel(db.Model):
    __modelname__ = "Group Member"

    __tablename__ = "group_members"
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    is_lead = db.Column(db.Boolean, default=False, nullable=False)
    permission = db.Column(db.Integer, default=Permission.READ, nullable=False)

    group = db.relationship(
        "GroupModel",
        backref=db.backref("members", cascade="delete, delete-orphan")
    )

    user = db.relationship(
        "UserModel",
        backref=db.backref("groups_membership", cascade="delete, delete-orphan")
    )

    @db.validates('is_lead')
    def validate_leader(self, key, is_lead):
        # We can only have one leader in a group
        if self.team.leader():
            raise ValueError(f"{self.group.name} group already have a leader")
        return is_lead
    
    @property
    def user_role(self):
        return f"{self.group.name}:{'leader' if self.is_lead else 'member'}"


  
class UserModel(BaseModel):
    __modelname__ = "User"

    __tablename__ = "users"
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    @classmethod
    def get_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"    

    def can(self, permission):
        return self.role is not None and \
            (self.role.permission and permission) == True
    
    def is_admin(self):
        return self.can(Permission.ADMINISTRATOR)
    
    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )
    




# {
#     "sub": 1 #userid,
#     "role": "User",
#     "groups": ["corecommerce:lead", "travel:member"],
#     "iat": "23/12/1995",
#     "exp": "29/30/1998"
# }

# @jwt_required
# @jwt_role("Administrator")
# @jwt_any_roles(["User", "Administrator"])