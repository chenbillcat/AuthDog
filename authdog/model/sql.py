import json

from sqlalchemy.exc import IntegrityError

from authdog.model.connection import get_engine, get_session_maker
from authdog.model.connection import get_session
from authdog.model.default import Domain, Project, User, Group, Role, \
    UserGroupMembership, UserRoleMembership, GroupRoleMembership
from authdog.common import exception


class DomainApi(object):
    """API for Domain model
    use the method in this class to
    work with Domain model
    """

    def __init__(self, session):
        self.session = session

    def _get_domain(self, domain_id):
        with self.session.begin(subtransactions=True):
            ref = self.session.query(Domain).filter_by(id=domain_id).first()  # return None or an object
            if ref is None:
                raise exception.DomainNotFound(domain_id=domain_id)
        return ref

    # return a dict or raise DomainNotFound
    def get_domain(self, domain_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_domain(domain_id)
        return ref.to_dict()

    # return a list of dicts
    def list_domains(self):
        with self.session.begin():
            refs = self.session.query(Domain).all()
            return [ref.to_dict() for ref in refs]

    # domain should be a dict
    # if domain already exist, raise Conflict
    def create_domain(self, domain):
        try:
            with self.session.begin():
                ref = Domain.from_dict(domain)
                self.session.add(ref)
                self.session.flush()
        except IntegrityError as e:
            raise exception.Conflict(
                type="Domain",
                details=json.dumps(domain) + ":" + e.message)

    # domain should be a dict
    def update_domain(self, domain_id, domain):
        try:
            with self.session.begin():
                ref = self._get_domain(domain_id)
                old_domain = ref.to_dict()
                for key in domain.keys():
                    old_domain[key] = domain[key]
                new_domain = Domain.from_dict(old_domain)
                for attr in Domain._attributes:
                    if attr != "id":
                        setattr(ref, attr, getattr(new_domain, attr))
                return ref.to_dict()
        except IntegrityError as e:
            raise exception.Conflict(
                type="Domain",
                details=json.dumps(domain) + ":" + e.message)

    def delete_domain(self, domain_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_domain(domain_id)
            try:
                self.session.delete(ref)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Constraint(
                    types="Domain",
                    details=domain_id + ":" + e.message)

    def list_projects_for_domain(self, domain_id):
        ref = self._get_domain(domain_id)
        projects = ref.project
        return [project.to_dict() for project in projects if project]

    def list_groups_for_domain(self, domain_id):
        ref = self._get_domain(domain_id)
        groups = ref.group
        return [group.to_dict() for group in groups if group]


class ProjectApi(object):
    """API for Project model
    use the method in this class to
    work with project model

    """

    def __init__(self, session):
        self.session = session

    def _get_project(self, project_id):
        with self.session.begin(subtransactions=True):
            ref = self.session.query(Project).filter_by(id=project_id).first()  # return None or an object
            if ref is None:
                raise exception.ProjectNotFound(project_id=project_id)
            return ref

    def get_project(self, project_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_project(project_id)
            return ref.to_dict()

    def list_projects(self):
        with self.session.begin():
            refs = self.session.query(Project).all()  # return a list with projects or empty list
            return [ref.to_dict() for ref in refs]

    # project should be a dict
    def create_project(self, project):
        with self.session.begin():
            try:
                ref = Project.from_dict(project)
                self.session.add(ref)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="Project",
                    details=json.dumps(project) + ":" + e.message)

    def update_project(self, project_id, project):
        try:
            with self.session.begin(subtransactions=True):
                ref = self._get_project(project_id)
                old_project = ref.to_dict()
                for key in project.keys():
                    old_project[key] = project[key]
                new_project = Project.from_dict(old_project)
                for attr in Project._attributes:
                    if attr != "id":
                        setattr(ref, attr, getattr(new_project, attr))
                return ref.to_dict()
        except IntegrityError as e:
            raise exception.Conflict(
                type="Project",
                details=json.dumps(project) + ":" + e.message)

    def delete_project(self, project_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_project(project_id)
            try:
                self.session.delete(ref)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Constraint(
                    type="Project",
                    details=project_id + ":" + e.message)

    def list_users_for_project(self, project_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_project(project_id)
            users = ref.user
            return [user.to_dict() for user in users if user]


class UserApi(object):
    """API for User model
    use the method in this class to
    work with user model

    """
    def __init__(self, session):
        self.session = session

    def _get_user(self, user_id):
        with self.session.begin(subtransactions=True):
            ref = self.session.query(User).filter_by(id=user_id).first()  # return None or an object
            if ref is None:
                raise exception.UserNotFound(user_id=user_id)
            return ref

    def get_user(self, user_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_user(user_id)
            return ref.to_dict()

    def list_users(self):
        with self.session.begin():
            refs = self.session.query(User).all()  # return a list with projects or empty list
            return [ref.to_dict() for ref in refs]

    # user should be a dict
    def create_user(self, user):
        with self.session.begin():
            try:
                ref = User.from_dict(user)
                self.session.add(ref)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="User",
                    details=json.dumps(user) + ":" + e.message)

    # user should be a dict
    def update_user(self, user_id, user):
        try:
            with self.session.begin(subtransactions=True):
                ref = self._get_user(user_id)
                old_user = ref.to_dict()
                for key in user.keys():
                    old_user[key] = user[key]
                new_user = User.from_dict(old_user)
                for attr in User._attributes:
                    if attr != "id":
                        setattr(ref, attr, getattr(new_user, attr))
                return ref.to_dict()
        except IntegrityError as e:
            raise exception.Conflict(
                type="User",
                details=json.dumps(user) + ":" + e.message)

    def delete_user(self, user_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_user(user_id)
            self.session.delete(ref)
            self.session.flush()

    def list_user_group_membership(self, user_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_user(user_id)
            ugms = ref.user_group_membership
            return [ugm.to_dict() for ugm in ugms if ugm]

    def list_user_role_membership(self, user_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_user(user_id)
            urms = ref.user_role_membership
            return [urm.to_dict() for urm in urms if urm]


class GroupApi(object):
    """API for Group model
    use the method in this class to
    work with group model

    """
    def __init__(self, session):
        self.session = session

    def _get_group(self, group_id):
        with self.session.begin(subtransactions=True):
            ref = self.session.query(Group).filter_by(id=group_id).first()  # return None or an object
            if ref is None:
                raise exception.GroupNotFound(group_id=group_id)
            return ref

    def get_group(self, group_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_group(group_id)
            return ref.to_dict()

    def list_groups(self):
        with self.session.begin():
            refs = self.session.query(Group).all()  # return a list with groups or empty list
            return [ref.to_dict() for ref in refs]

    def create_group(self, group):
        with self.session.begin():
            try:
                ref = Group.from_dict(group)
                self.session.add(ref)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="Group",
                    details=json.dumps(group) + ":" + e.message)

    # group should be a dict
    def update_group(self, group_id, group):
        try:
            with self.session.begin(subtransactions=True):
                ref = self._get_group(group_id)
                old_group = ref.to_dict()
                for key in group.keys():
                    old_group[key] = group[key]
                new_group = Group.from_dict(old_group)
                for attr in Group._attributes:
                    if attr != "id":
                        setattr(ref, attr, getattr(new_group, attr))
                return ref.to_dict()
        except IntegrityError as e:
            raise exception.Conflict(
                type="Group",
                details=json.dumps(group) + ":" + e.message)

    def delete_group(self, group_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_group(group_id)
            self.session.delete(ref)
            self.session.flush()

    def list_user_group_membership(self, group_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_group(group_id)
            ugms = ref.user_group_membership
            return [ugm.to_dict() for ugm in ugms if ugm]

    def list_group_role_membership(self, group_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_group(group_id)
            grms = ref.group_role_membership
            return [grm.to_dict() for grm in grms if grm]


class RoleApi(object):
    """API for Role model
    use the method in this class to
    work with role model

    """

    def __init__(self, session):
        self.session = session

    def _get_role(self, role_id):
        with self.session.begin(subtransactions=True):
            ref = self.session.query(Role).filter_by(id=role_id).first()  # return None or an object
            if ref is None:
                raise exception.RoleNotFound(role_id=role_id)
            return ref

    def get_role(self, role_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_role(role_id)
            return ref.to_dict()

    def list_roles(self):
        with self.session.begin():
            refs = self.session.query(Role).all()  # return a list with groups or empty list
            return [ref.to_dict() for ref in refs]

    # role should be a dict
    def create_role(self, role):
        with self.session.begin():
            try:
                ref = Role.from_dict(role)
                self.session.add(ref)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="Role",
                    details=json.dumps(role) + ":" + e.message)

    # role should be a dict
    def update_role(self, role_id, role):
        try:
            with self.session.begin(subtransactions=True):
                ref = self._get_role(role_id)
                old_role = ref.to_dict()
                for key in role.keys():
                    old_role[key] = role[key]
                new_role = Role.from_dict(old_role)
                for attr in Role._attributes:
                    if attr != "id":
                        setattr(ref, attr, getattr(new_role, attr))
                return ref.to_dict()
        except IntegrityError as e:
            raise exception.Conflict(
                type="Role",
                details=json.dumps(role) + ":" + e.message)

    def delete_role(self, role_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_role(role_id)
            self.session.delete(ref)
            self.session.flush()

    def list_user_role_membership(self, role_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_role(role_id)
            urms = ref.user_role_membership
            return [urm.to_dict() for urm in urms if urm]

    def list_group_role_membership(self, role_id):
        with self.session.begin(subtransactions=True):
            ref = self._get_role(role_id)
            urms = ref.group_role_membership
            return [urm.to_dict() for urm in urms if urm]


class RelationshipApi(object):

    def __init__(self, session):
        self.session = session

    def bind_user_to_group(self, user_id, group_id):
        with self.session.begin():
            try:
                user_group_membership = UserGroupMembership.from_dict(
                    {"user_id": user_id, "group_id": group_id})
                self.session.add(user_group_membership)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="UserGroupMembership",
                    details=user_id +":" + group_id + ":" + e.message)

    def bind_role_to_user(self, role_id, user_id):
        with self.session.begin():
            try:
                user_role_membership = UserRoleMembership.from_dict(
                    {"user_id": user_id, "role_id": role_id})
                self.session.add(user_role_membership)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="UserRoleMembership",
                    details=user_id +":" + role_id + ":" + e.message)

    def bind_role_to_group(self, role_id, group_id):
        with self.session.begin():
            try:
                group_role_membership = GroupRoleMembership.from_dict(
                    {"group_id": group_id, "role_id": role_id})
                self.session.add(group_role_membership)
                self.session.flush()
            except IntegrityError as e:
                raise exception.Conflict(
                    type="GroupRoleMembership",
                    details=group_id +":" + role_id + ":" + e.message)
