
from . import api
from flask_restplus import Resource


from ...parser import pagination

@api.route("/")
class GroupCollection(Resource):
    
    def get(self):
        """ Display All Available Group """
        return {}

@api.route("/<string:group_id>/")
class GroupDetail(Resource):

    def get(self, group_id):
        """ Show Detail Group by Selected Group ID """
        return {}

    def put(self, group_id):
        """ Update Group Information by Selected Group ID """
        return {}

    def delete(self, group_id):
        """ Delete Group by Selected Group ID """
        return {}

@api.route("/<string:group_id>/members/")
class GroupMemberCollection(Resource):

    def get(self, group_id):
        """ Get group members by group ID """
        return {}

    def post(self, group_id):
        """ Add new member to a group """
        return {}

@api.route("/<string:group_id>/members/<string:user_id>/")
class GroupMemberInfo(Resource):

    def get(self, group_id):
        """ Get group members by group ID """
        return {}

    def post(self, group_id):
        """ Add new member to a group """
        return {}