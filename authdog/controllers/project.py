# coding:utf-8
from pecan import expose
from pecan.rest import RestController


class ProjectsController(RestController):

    @expose('json')
    def get_all(self):
        pass
        return dict()

    @expose('json')
    def post(self):
        pass
        return dict()

    @expose('json')
    def get_one(self, project_id):
        pass
        return dict()

    @expose('json')
    @expose(method="PATCH")
    def patch(self, project_id):
        pass
        return dict()

    @expose('json')
    def delete(self, project_id):
        pass
        return dict()
