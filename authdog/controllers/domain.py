# coding:utf-8
from pecan import expose
from pecan.rest import RestController


class DomainsController(RestController):

    @expose("json")
    def get_all(self):
        pass
        return dict()

    @expose("json") 
    def get_one(self, domain_id):
        pass
        # return "/domains/%s"%id

    @expose("json")
    def post(self):
        pass
        # return "/domains"

    @expose("json")
    @expose(method="PATCH")
    def patch(self, domain_id):
        pass
        # return "/domains"

    @expose("json")
    def delete(self, domain_id):
        pass
        # return "/domains/id"
