class Error(Exception):
    """Base error class.

        Child classes should define an HTTP status code, title, and a
        message_format.

    """
    code = None
    title = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        message = self._build_message(message, **kwargs)
        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        try:
            if message:
                return message
            else:
                return self.message_format % kwargs
        except Exception as e:
            return e.message


class NotFound(Error):
    message_format = "Could not find: %(target)s"
    code = 404
    title = 'Not Found'


class Conflict(Error):
    message_format = "Conflict occurred attempting to store %(type)s: %(details)s"
    code = 409
    title = 'Conflict'


class JsonError(Error):
    message_format = "extra cant not be encode to json: %(details)s"
    code = 500
    title = 'Json'


class Constraint(Error):
    message_format = "a foreign key constraint fails when delete: %(type)s: %(details)s"
    code = 500
    title = 'constraint'


class DomainNotFound(NotFound):
    message_format = "Cound not find domain: %(domain_id)s"


# usage: raise ProjectNotFound(project_id=id)
class ProjectNotFound(NotFound):
    message_format = "Cound not find project: %(project_id)s"


# usage: raise UserNotFound(user_id=id)
class UserNotFound(NotFound):
    message_format = "Cound not find user: %(user_id)s"


# usage: raise GroupNotFound(group_id=id)
class GroupNotFound(NotFound):
    message_format = "Cound not find group: %(group_id)s"


# usage: raise RoleNotFound(role_id=id)
class RoleNotFound(NotFound):
    message_format = "Cound not find role: %(role_id)s"
