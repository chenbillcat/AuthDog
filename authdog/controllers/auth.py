from pecan import expose
from pecan.rest import RestController
from pecan import response


class TokenController(RestController):

    @expose('json')
    def post(self):
        pass

    @expose()
    def _default(self):
        response.status = 404
        pass


class AuthController(RestController):

    tokens = TokenController()

    @expose()
    def _default(self):
        response.status = 404
        pass
