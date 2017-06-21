# coding:utf-8
from unittest import TestCase
from webtest import TestApp

from pecan import conf

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.expression import text

from authdog.tests import FunctionalTest
from authdog.model import SessionFactory, DatabaseEngine
from authdog.model import api
from authdog.model import default as default_model


class TestCreateDefaultTables(FunctionalTest):

    def test_create_default_all(self):
        engine = api.get_engine()
        session = api.get_session()
        default_model.Base.metadata.create_all(engine)

        domain = default_model.Domain(id="1", name="test_domain", enabled=1)
        project = default_model.Project(
            id="1",
            name="test_project",
            extra='{"hello":"world"}',
            enabled=1,
            description="this is a test project",
            domain_id=domain.id)
        user = default_model.User(
            id="1",
            name="test_user",
            password="qazwsx",
            extra='{"hello":"world"}',
            enabled=1,
            project_id=project.id)
        group = default_model.Group(
            id="1",
            name="test_group",
            extra='{"hello":"world"}',
            description="this is a test group",
            domain_id=domain.id
        )
        role = default_model.Role(
            id="1",
            name="test_role",
            extra='{"hello":"world"}',
            description="this is a test role",
        )
        user_group_m = default_model.UserGroupMembership(
            user_id=user.id,
            group_id=group.id
        )
        user_role_m = default_model.UserRoleMembership(
            user_id=user.id,
            role_id=role.id
        )
        group_role_m = default_model.GroupRoleMembership(
            group_id=group.id,
            role_id=role.id
        )
        # sessionmaker(bind=engine, autocommit=True)

        with session.begin():
            session.add(domain)
            session.add(project)
            session.add(user)
            session.add(group)
            session.add(role)
            session.add(user_group_m)
            session.add(user_role_m)
            session.add(group_role_m)

        domain_result = session.query(default_model.Domain).first()
        result = domain_result.to_dict()
        assert result['name'] == "test_domain"

        project_result = session.query(default_model.Project).first()
        result = project_result.to_dict()
        assert result['name'] == "test_project"

        user_result = session.query(default_model.User).first()
        result = user_result.to_dict()
        assert result['name'] == "test_user"

        group_result = session.query(default_model.Group).first()
        result = group_result.to_dict()
        assert result['name'] == "test_group"

        role_result = session.query(default_model.Role).first()
        result = role_result.to_dict()
        assert result['name'] == "test_role"

        user_group_m_result = session.query(default_model.UserGroupMembership).first()
        result = user_group_m_result.to_dict()
        assert result['user_id'] == "1"
        assert result['group_id'] == "1"

        user_role_m_result = session.query(default_model.UserRoleMembership).first()
        result = user_role_m_result.to_dict()
        assert result['user_id'] == "1"
        assert result['role_id'] == "1"

        group_role_m_result = session.query(default_model.GroupRoleMembership).first()
        result = group_role_m_result.to_dict()
        assert result['group_id'] == "1"
        assert result['role_id'] == "1"

        default_model.Base.metadata.drop_all(engine)
