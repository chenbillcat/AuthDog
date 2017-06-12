from pecan import expose, redirect
from webob.exc import status_map

from authdog.controllers.auth import AuthController
from authdog.controllers.domain import DomainsController
from authdog.controllers.group import GroupsController
from authdog.controllers.project import ProjectsController
from authdog.controllers.user import UsersController


class RootController(object):

    auth = AuthController()
    domains = DomainsController()
    groups = GroupsController()
    projects = ProjectsController()
    users = UsersController()

    @expose(generic=True, template='index.html')
    def index(self):
        return dict()

    @index.when(method='POST')
    def index_post(self, q):
        redirect('https://pecan.readthedocs.io/en/latest/search.html?q=%s' % q)

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
