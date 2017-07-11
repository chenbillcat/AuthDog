# coding:utf-8
import os


from pecan import conf
from pecan import set_config
from pecan.testing import load_test_app

from authdog.tests import FunctionalTest
from authdog.model import connection
from authdog.model import default as default_model
from authdog.tests.test_model_default import CreateTableTest
from authdog.model.sql import DomainApi, ProjectApi, UserApi, GroupApi, RoleApi
from authdog.common import exception


def get_domain_data():
    domain1 = default_model.Domain(id="1", name="test_domain1", enabled=1)
    domain2 = default_model.Domain(id="2", name="test_domain2", enabled=1)
    domain3 = default_model.Domain(id="3", name="test_domain3", enabled=0)
    domain4 = default_model.Domain(id="4", name="test_domain4", enabled=0)
    return [domain1, domain2, domain3, domain4]


def get_project_data():
    project1 = default_model.Project(
            id="1",
            name="test_project1",
            extra='{"test": "test_project1"}',
            enabled=1,
            description="this is test_project1",
            domain_id="1")
    project2 = default_model.Project(
            id="2",
            name="test_project2",
            extra='{"test": "test_project2"}',
            enabled=1,
            description="this is test_project2",
            domain_id="1")
    project3 = default_model.Project(
            id="3",
            name="test_project3",
            extra='{"test": "test_project3"}',
            enabled=1,
            description="this is test_project3",
            domain_id="2")
    project4 = default_model.Project(
            id="4",
            name="test_project4",
            extra='{"test": "test_project4"}',
            enabled=1,
            description="this is test_project4",
            domain_id="2")
    return [project1, project2, project3, project4]


def get_group_data():
    group1 = default_model.Group(
        id="1",
        name="test_group1",
        extra='{"test": "test_group1"}',
        description="this is a test group1",
        domain_id="1")
    group2 = default_model.Group(
        id="2",
        name="test_group2",
        extra='{"test": "test_group2"}',
        description="this is a test group",
        domain_id="1")
    return [group1, group2]


def get_user_data():
    user1 = default_model.User(
        id="1",
        name="test_user1",
        password="qazwsx",
        extra='{"user":"test_user1"}',
        enabled=1,
        project_id="1")
    user2 = default_model.User(
        id="2",
        name="test_user2",
        password="qazwsx",
        extra='{"user":"test_user2"}',
        enabled=1,
        project_id="1")
    user3 = default_model.User(
        id="3",
        name="test_user3",
        password="qazwsx",
        extra='{"user":"test_user3"}',
        enabled=1,
        project_id="2")
    user4 = default_model.User(
        id="4",
        name="test_user4",
        password="qazwsx",
        extra='{"user":"test_user4"}',
        enabled=1,
        project_id="2")
    user5 = default_model.User(
        id="5",
        name="test_user5",
        password="qazwsx",
        extra='{"user":"test_user5"}',
        enabled=1,
        project_id="2")
    return [user1, user2, user3, user4, user5]


def get_role_data():
    role1 = default_model.Role(
        id="1",
        name="test_role1",
        extra='{"test": "role1"}',
        description="hello world")
    role2 = default_model.Role(
        id="2",
        name="test_role2",
        extra='{"test": "role2"}',
        description="hello world")
    role3 = default_model.Role(
        id="3",
        name="test_role3",
        extra='{"test": "role3"}',
        description="hello world")
    return [role1, role2, role3]


def get_user_group_membership():
    ugm1 = default_model.UserGroupMembership(
        user_id="1",
        group_id="1"
    )
    ugm2 = default_model.UserGroupMembership(
        user_id="2",
        group_id="1"
    )
    ugm3 = default_model.UserGroupMembership(
        user_id="3",
        group_id="2"
    )
    ugm4 = default_model.UserGroupMembership(
        user_id="4",
        group_id="2"
    )
    return [ugm1, ugm2, ugm3, ugm4]


def get_user_role_membership():
    urm1 = default_model.UserRoleMembership(
        user_id="1",
        role_id="1"
    )
    urm2 = default_model.UserRoleMembership(
        user_id="1",
        role_id="2"
    )
    urm3 = default_model.UserRoleMembership(
        user_id="2",
        role_id="1"
    )
    urm4 = default_model.UserRoleMembership(
        user_id="3",
        role_id="2"
    )
    urm5 = default_model.UserRoleMembership(
        user_id="4",
        role_id="3"
    )
    return [urm1, urm2, urm3, urm4, urm5]


def get_group_role_membership():
    grm1 = default_model.GroupRoleMembership(
        group_id="1",
        role_id="1"
    )
    grm2 = default_model.GroupRoleMembership(
        group_id="1",
        role_id="2"
    )
    grm3 = default_model.GroupRoleMembership(
        group_id="2",
        role_id="1"
    )
    grm4 = default_model.GroupRoleMembership(
        group_id="2",
        role_id="2"
    )
    grm5 = default_model.GroupRoleMembership(
        group_id="2",
        role_id="3"
    )
    return [grm1, grm2, grm3, grm4, grm5]


def write_domain_data():
    session = connection.get_session()
    domains = get_domain_data()
    with session.begin():
        for domain in domains:
            session.add(domain)
            session.flush()
    return session


def write_project_data():
    session = connection.get_session()
    projects = get_project_data()
    with session.begin():
        for project in projects:
            session.add(project)
            session.flush()
    return session


def write_group_data():
    session = connection.get_session()
    groups = get_group_data()
    with session.begin():
        for group in groups:
            session.add(group)
            session.flush()
    return session


def write_user_data():
    session = connection.get_session()
    users = get_user_data()
    with session.begin():
        for user in users:
            session.add(user)
            session.flush()
    return session


def write_role_data():
    session = connection.get_session()
    roles = get_role_data()
    with session.begin():
        for role in roles:
            session.add(role)
            session.flush()
    return session


def write_user_group_membership():
    session = connection.get_session()
    ugms = get_user_group_membership()
    with session.begin():
        for u in ugms:
            session.add(u)
            session.flush()
    return session


def write_user_role_membership():
    session = connection.get_session()
    urms = get_user_role_membership()
    with session.begin():
        for u in urms:
            session.add(u)
            session.flush()
    return session


def write_group_role_membership():
    session = connection.get_session()
    grms = get_group_role_membership()
    with session.begin():
        for g in grms:
            session.add(g)
            session.flush()
    return session


def write_test_data():
    write_domain_data()
    write_project_data()
    write_group_data()
    write_user_data()
    write_role_data()
    write_user_group_membership()
    write_user_role_membership()
    write_group_role_membership()


class TestDomainApi(CreateTableTest):

    def test_get_domain(self):
        session = write_domain_data()
        domain_api = DomainApi(session)
        result = domain_api.get_domain("1")
        assert result.get("name") == "test_domain1"

    def test_list_domains(self):
        session = write_domain_data()
        domain_api = DomainApi(session)
        result = domain_api.list_domains()
        assert len(result) == 4

    def test_list_domains_empty_table(self):
        session = connection.get_session()
        domain_api = DomainApi(session)
        result = domain_api.list_domains()
        assert isinstance(result, list)

    def test_create_domains(self):
        session = connection.get_session()
        domain_api = DomainApi(session)
        for domain in get_domain_data():
            domain = domain.to_dict()
            domain_api.create_domain(domain)
        result = domain_api.list_domains()
        assert isinstance(result, list)
        assert len(result) == 4

    def test_create_domain_conflict(self):
        session = connection.get_session()
        domain_api = DomainApi(session)
        for domain in get_domain_data():
            domain = domain.to_dict()
            domain_api.create_domain(domain)
        domain = get_domain_data()[0]
        domain = domain.to_dict()
        try:
            domain_api.create_domain(domain)
        except Exception as e:
            assert isinstance(e, exception.Conflict)

    def test_update_domain(self):
        session = connection.get_session()
        domain_api = DomainApi(session)
        for domain in get_domain_data():
            domain = domain.to_dict()
            domain_api.create_domain(domain)
        domain = {"name": "test_domain4_update", "enabled": 1}
        domain_api.update_domain(domain_id="4", domain=domain)
        ref = domain_api.get_domain(domain_id="4")
        assert ref.get("name") == "test_domain4_update"

    def test_update_domain_conflict(self):
        session = connection.get_session()
        domain_api = DomainApi(session)
        for domain in get_domain_data():
            domain = domain.to_dict()
            domain_api.create_domain(domain)
        domain = {"name": "test_domain3", "enabled": 1}
        try:
            ref = domain_api.update_domain(domain_id="4", domain=domain)
        except Exception as e:
            assert isinstance(e, exception.Conflict)

    def test_delete_domain(self):
        write_domain_data()
        session = connection.get_session()
        domain_api = DomainApi(session)
        domains = domain_api.list_domains()
        assert len(domains) == 4
        for domain in get_domain_data():
            domain_id = domain.to_dict().get("id")
            domain_api.delete_domain(domain_id)
        domains = domain_api.list_domains()
        assert len(domains) == 0

        write_test_data()
        domain_id = "1"
        try:
            domain_api.delete_domain(domain_id)
        except exception.Constraint as e:
            assert isinstance(e, exception.Constraint)
        else:
            raise Exception("Constraint didn't happen")

    def test_list_projects_for_domain(self):
        write_domain_data()
        write_project_data()
        session = connection.get_session()
        domain_id = "1"
        domain_api = DomainApi(session)
        projects = domain_api.list_projects_for_domain(domain_id)
        assert len(projects) == 2

    def test_list_groups_for_domain(self):
        write_domain_data()
        write_group_data()
        session = connection.get_session()
        domain_id = "1"
        domain_api = DomainApi(session)
        groups = domain_api.list_groups_for_domain(domain_id)
        assert len(groups) == 2


class TestProjectApi(CreateTableTest):

    def test_get_project(self):
        write_test_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        project = project_api.get_project("1")
        assert project.get("name") == "test_project1"

    def test_list_projects(self):
        write_test_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        projects = project_api.list_projects()
        assert len(projects) == 4
        assert projects[0].get("id") == "1"

    def test_create_project(self):
        write_domain_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        projects = get_project_data()
        for project in projects:
            project = project.to_dict()
            project_api.create_project(project)
        refs = project_api.list_projects()
        assert len(refs) == 4
        assert refs[0].get("id") == "1"

    def test_create_project_conflict(self):
        write_domain_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        projects = get_project_data()
        for project in projects:
            project = project.to_dict()
            project_api.create_project(project)
        try:
            project_api.create_project(projects[0].to_dict())
        except Exception as e:
            assert isinstance(e, exception.Conflict)

    def test_update_project(self):
        write_test_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        project = {"extra": '{"test": "test_project2_update_project"}', "main": "test"}
        project_api.update_project(project_id="1", project=project)
        ref = project_api.get_project(project_id="1")
        assert ref.get("extra").get("main") == "test"

    def test_update_project_conflict(self):
        write_test_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        project = {"name": "test_project2"}
        try:
            project_api.update_project(project_id="1", project=project)
        except Exception as e:
            assert isinstance(e, exception.Conflict)

    def test_delete_project(self):
        write_domain_data()
        write_project_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        projects = project_api.list_projects()
        assert len(projects) == 4
        for i in get_project_data():
            project_api.delete_project(i.to_dict().get("id"))
        projects = project_api.list_projects()
        assert len(projects) == 0

        write_project_data()
        write_user_data()
        try:
            project_api.delete_project(project_id="1")
        except exception.Constraint as e:
            assert isinstance(e, exception.Constraint)
        else:
            raise Exception("Constraint didn't happen")

    def test_list_users_for_project(self):
        write_test_data()
        session = connection.get_session()
        project_api = ProjectApi(session)
        users = project_api.list_users_for_project(project_id="1")
        assert len(users) == 2


class TestUserApi(CreateTableTest):

    def test_get_user(self):
        write_test_data()
        session = connection.get_session()
        user_api = UserApi(session)
        user = user_api.get_user(user_id="1")
        assert user.get("name") == "test_user1"

        try:
            user = user_api.get_user(user_id="10")
        except exception.UserNotFound as e:
            assert isinstance(e, exception.UserNotFound)

    def test_list_users(self):
        # test the empty user table
        session = connection.get_session()
        user_api = UserApi(session)
        users = user_api.list_users()
        assert isinstance(users, list)
        assert len(users) == 0

        write_test_data()
        users = user_api.list_users()
        assert isinstance(users, list)
        assert len(users) == 5

    # user should be a dict
    def test_create_user(self):
        write_domain_data()
        write_project_data()
        session = connection.get_session()

        user_api = UserApi(session)
        for user in get_user_data():
            user = user.to_dict()
            user_api.create_user(user)
        users = user_api.list_users()
        assert len(users) == 5

        for user in get_user_data():
            try:
                user = user.to_dict()
                user_api.create_user(user)
            except Exception as e:
                assert isinstance(e, exception.Conflict)

    # user should be a dict
    def test_update_user(self):
        write_test_data()
        session = connection.get_session()
        user_api = UserApi(session)

        user = {"name": "test_user20"}
        user_api.update_user(user_id="2", user=user)
        u = user_api.get_user(user_id="2")
        assert u.get("name") == "test_user20"

        user = {"name": "test_user3"}
        try:
            user_api.update_user(user_id="1", user=user)
        except exception.Conflict as e:
            assert isinstance(e, exception.Conflict)
        else:
            raise Exception("Conflict didn't happen")

    def test_delete_user(self):
        write_domain_data()
        write_project_data()
        write_group_data()
        write_user_data()
        write_role_data()

        session = connection.get_session()
        user_api = UserApi(session)
        users = get_user_data()
        for user in users:
            user_id = user.to_dict().get("id")
            user_api.delete_user(user_id)
        users = user_api.list_users()
        assert len(users) == 0

        try:
            user_api.delete_user(user_id="1")
        except exception.UserNotFound as e:
            assert isinstance(e, exception.UserNotFound)
        else:
            raise Exception("Delete user failed didn't happen")

        write_user_data()
        write_user_group_membership()
        write_user_role_membership()
        write_group_role_membership()

        with session.begin():
            ugms = session.query(default_model.UserGroupMembership).filter_by(user_id="1").all()
            assert len(ugms) != 0

        user_api.delete_user(user_id="1")

        with session.begin():
            ugms = session.query(default_model.UserGroupMembership).filter_by(user_id="1").all()
            assert len(ugms) == 0

    def test_list_user_group_membership(self):
        write_test_data()
        session = connection.get_session()
        user_api = UserApi(session)
        ugms = user_api.list_user_group_membership(user_id="1")
        assert len(ugms) == 1

    def test_list_user_role_membership(self):
        write_test_data()
        session = connection.get_session()
        user_api = UserApi(session)
        urms = user_api.list_user_role_membership(user_id="1")
        assert len(urms) == 2


class TestGroupApi(CreateTableTest):

    def test_get_group(self):
        write_test_data()
        session = connection.get_session()
        group_api = GroupApi(session)
        group = group_api.get_group(group_id="1")
        assert group.get("name") == "test_group1"

        try:
            group = group_api.get_group(group_id="5")
        except exception.GroupNotFound as e:
            assert isinstance(e, exception.GroupNotFound)
        else:
            raise Exception("GroupNotFound didn't happen")

    def test_list_groups(self):
        session = connection.get_session()
        group_api = GroupApi(session)
        groups = group_api.list_groups()
        assert len(groups) == 0

        write_test_data()
        groups = group_api.list_groups()
        assert len(groups) == 2

    def test_create_group(self):
        write_domain_data()
        write_project_data()
        groups = get_group_data()
        session = connection.get_session()
        group_api = GroupApi(session)
        for g in groups:
            group = g.to_dict()
            group_api.create_group(group)

        groups = group_api.list_groups()
        assert len(groups) == 2

    def test_update_group(self):
        write_test_data()
        session = connection.get_session()
        group_api = GroupApi(session)
        group = {"name": "group_update"}
        group_api.update_group("2", group)
        g = group_api.get_group("2")
        assert g.get("name") == "group_update"

        try:
            group = {"name": "test_group1"}
            group_api.update_group("2", group)
        except exception.Conflict as e:
            assert isinstance(e, exception.Conflict)
        else:
            raise Exception("Conflict didn't happen")

    def test_delete_group(self):
        write_test_data()
        session = connection.get_session()
        group_api = GroupApi(session)
        ugms = group_api.list_user_group_membership(group_id="2")
        assert len(ugms) == 2
        grms = group_api.list_group_role_membership(group_id="2")
        assert len(grms) == 3

        group_api.delete_group(group_id="2")
        try:
            group = group_api.get_group(group_id="2")
        except exception.GroupNotFound as e:
            assert isinstance(e, exception.GroupNotFound)
        else:
            raise Exception("GroupNotFound didn't happen")

        ugms = session.query(default_model.UserGroupMembership).filter_by(group_id="2").all()
        assert len(ugms) == 0
        grms = session.query(default_model.GroupRoleMembership).filter_by(group_id="2").all()
        assert len(grms) == 0

    def test_list_user_group_membership(self):
        write_test_data()
        session = connection.get_session()
        group_api = GroupApi(session)
        ugms = group_api.list_user_group_membership(group_id="2")
        assert len(ugms) == 2

    def test_list_group_role_membership(self):
        write_test_data()
        session = connection.get_session()
        group_api = GroupApi(session)
        grms = group_api.list_group_role_membership(group_id="2")
        assert len(grms) == 3


class TestRoleApi(CreateTableTest):

    def test_get_role(self):
        write_test_data()
        session = connection.get_session()
        role_api = RoleApi(session)
        role = role_api.get_role(role_id="1")
        assert role.get("name") == "test_role1"

        try:
            role = role_api.get_role(role_id="10")
        except exception.RoleNotFound as e:
            assert isinstance(e, exception.RoleNotFound)

    def test_list_roles(self):
        write_test_data()
        session = connection.get_session()
        role_api = RoleApi(session)
        roles = role_api.list_roles()
        assert len(roles) == 3

    def test_create_role(self):
        write_domain_data()
        write_project_data()
        write_group_data()
        write_user_data()

        session = connection.get_session()
        role_api = RoleApi(session)

        roles = role_api.list_roles()
        assert len(roles) == 0

        roles = get_role_data()
        for r in roles:
            role = r.to_dict()
            role_api.create_role(role)
        roles = role_api.list_roles()
        assert len(roles) == 3

    def test_update_role(self):
        write_test_data()

        session = connection.get_session()
        role_api = RoleApi(session)
        role = {"name": "test_role1_update"}
        role_api.update_role("1", role)
        role = role_api.get_role("1")
        assert role.get("name") == "test_role1_update"

        try:
            role = {"name": "test_role2"}
            role_api.update_role("1", role)
        except exception.Conflict as e:
            assert isinstance(e, exception.Conflict)
        else:
            raise Exception("Conflict didn't happen")

    def test_delete_role(self):
        write_test_data()

        session = connection.get_session()
        role_api = RoleApi(session)

        urms = role_api.list_user_role_membership(role_id="2")
        assert len(urms) == 2
        grms = role_api.list_group_role_membership(role_id="2")
        assert len(grms) == 2

        role_api.delete_role(role_id="2")
        try:
            group = role_api.get_role(role_id="2")
        except exception.RoleNotFound as e:
            assert isinstance(e, exception.RoleNotFound)
        else:
            raise Exception("RoleNotFound didn't happen")

        ugms = session.query(default_model.UserRoleMembership).filter_by(role_id="2").all()
        assert len(ugms) == 0
        grms = session.query(default_model.GroupRoleMembership).filter_by(role_id="2").all()
        assert len(grms) == 0

    def test_list_user_role_membership(self):
        write_test_data()
        session = connection.get_session()
        role_api = RoleApi(session)
        urms = role_api.list_user_role_membership(role_id="2")
        assert len(urms) == 2

    def test_list_group_role_membership(self):
        write_test_data()
        session = connection.get_session()
        role_api = RoleApi(session)
        grms = role_api.list_group_role_membership(role_id="2")
        assert len(grms) == 2
