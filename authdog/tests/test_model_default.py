# coding:utf-8
import os
import json

from unittest import TestCase
from webtest import TestApp

from pecan import conf
from pecan import set_config
from pecan.testing import load_test_app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.expression import text

from authdog.tests import FunctionalTest
from authdog.model import connection
from authdog.model import default as default_model


class CreateTableTest(FunctionalTest):

    def setUp(self):
        self.app = load_test_app(os.path.join(
            os.path.dirname(__file__),
            'config.py'
        ))
        engine = connection.get_engine()
        # try to clear test tables first before create all tables
        default_model.Base.metadata.drop_all(engine)
        default_model.Base.metadata.create_all(engine)

    def tearDown(self):
        engine = connection.get_engine()
        set_config({}, overwrite=True)
        default_model.Base.metadata.drop_all(engine)


class TestCreateDefaultTables(CreateTableTest):

    def test_create_default_all(self):
        # engine = connection.get_engine()
        session = connection.get_session()
        # default_model.Base.metadata.create_all(engine)

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
            extra='{"extra0":"extra0"}',
            enabled=1,
            project_id=project.id,
            domain_id=domain.id)
        user1 = default_model.User(
            id="2",
            name="test_user2",
            password="qazwsx",
            extra='{"hello":"world"}',
            enabled=1,
            project_id=project.id,
            domain_id=domain.id)

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

        def get_user_dict(**kwargs):
            return kwargs

        def from_dict(cls, d):
            new_d = d.copy()
            import json
            # import pdb; pdb.set_trace()
            if getattr(cls, "extra", None):
                new_d["extra"] = {key: new_d.pop(key)
                                  for key in d.keys()
                                  if key not in cls._attributes and key != "extra"}
                extra_json = json.loads(d.get("extra"))
                new_d["extra"].update(extra_json)
                new_d["extra"] = json.dumps(new_d["extra"])
            else:
                for key in d.keys():
                    if key not in cls._attributes:
                        new_d.pop(key)
            return cls(**new_d)

        user3 = get_user_dict(
            id="3",
            name="test_user3",
            password="qazwsx",
            extra={"extra0":1},
            enabled=1,
            project_id=project.id,
            domain_id=domain.id,
            extra1="extra1",
            extra2="extra2")
        # user3 = from_dict(default_model.User, user3)
        user3 = default_model.User.from_dict(user3)


        with session.begin():
            session.add(domain)
            session.add(project)
            session.add(user)
            session.add(user1)
            session.add(user3)
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


        user3_result = session.query(default_model.User).filter_by(id=3).first()
        result3 = user3_result.to_dict()
        assert result3["id"] == "3"
        assert isinstance(result3["extra"], dict)

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

        # default_model.Base.metadata.drop_all(engine)


class TestScopedSessionWithEventlet(FunctionalTest):

    def get_session(self):
        session = connection.get_session()
        return id(session), session

    def test_scoped_session_with_eventlet(self):
        import eventlet
        coroutine1 = eventlet.spawn(self.get_session)
        coroutine2 = eventlet.spawn(self.get_session)
        id1, session1 = coroutine1.wait()
        id2, sessoin2 = coroutine2.wait()
        print id1, id2
        assert session1 is sessoin2
        assert id1 != id2
        self.assertNotEqual(id1, id2)


