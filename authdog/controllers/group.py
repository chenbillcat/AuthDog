from pecan import expose
from pecan.rest import RestController
from pecan import response


class UsersController(RestController):

    @expose('json')
    def get(self, group_id):
        pass
        return dict()

    @expose('json')
    def put(self, group_id, user_id):
        pass
        return dict()

    @expose('json')
    @expose(method="HEAD")
    def head(self, group_id, user_id):
        pass
        return dict()

    @expose('json')
    def delete(self, group_id, user_id):
        pass
        return dict()


class GroupsController(RestController):

    users = UsersController()

    @expose('json')
    def get_all(self):
        pass
        return dict()

    @expose('json')
    def post(self):
        pass
        return dict()

    @expose('json')
    def get_one(self, group_id):
        pass
        return dict()

    @expose('json')
    @expose(method="PATCH")
    def patch(self, group_id):
        pass
        return dict(hello="wolrd")

    @expose('json')
    def delete(self, group_id):
        pass
        return dict()
