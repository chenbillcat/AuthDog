# coding:utf-8
from pecan import expose
from pecan.rest import RestController


class ProjectsController(RestController):

    @expose('json')
    def get(self, user_id):
        pass
        return dict()


class GroupsController(RestController):

    @expose('json')
    def get(self, user_id):
        pass
        return dict()


class UsersController(RestController):

    projects = ProjectsController()
    groups = GroupsController()

    @expose('json')
    def get_all(self):
        pass
        return dict()

    @expose('json')
    def post(self):
        pass
        return dict()

    @expose('json')
    def get_one(self, user_id):
        pass
        return dict()

    @expose('json')
    @expose(method="PATCH")
    def patch(self, user_id):
        pass
        return dict()

    @expose('json')
    def delete(self, user_id):
        pass
        return dict()
