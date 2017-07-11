# coding:utf-8
import json

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, Text, ForeignKey
from sqlalchemy.orm import relationship

from authdog.common import exception

Base = declarative_base()


def to_dict(self):
    result = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    if "extra" in result.keys():
        result["extra"] = json.loads(result.get("extra"))
    return result


class BaseDict(object):

    _attributes = None

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()

        if getattr(cls, "extra", None):
            new_d["extra"] = {key: new_d.pop(key)
                              for key in d.keys()
                              if key not in cls._attributes and key != "extra"}
            extra_json = {}
            try:
                if isinstance(d.get("extra"), str):
                    extra_json = json.loads(d.get("extra"))
                if isinstance(d.get("extra"), dict):
                    extra_json = d.get("extra")
            except Exception:
                raise exception.JsonError(details=d.get("extra"))
            new_d["extra"].update(extra_json)
            new_d["extra"] = json.dumps(new_d["extra"])
        else:
            for key in d.keys():
                if key not in cls._attributes:
                    new_d.pop(key)
        return cls(**new_d)


Base.to_dict = to_dict


class Domain(Base, BaseDict):
    __tablename__ = "domain"
    _attributes = ['id', 'name', 'enabled']

    id = Column(String(64), primary_key=True, nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, unique=True)
    enabled = Column(SmallInteger)

    project = relationship("Project", backref="domain")
    group = relationship("Group", backref="domain")

    def __repr__(self):
        return "<Domain(id='%s', name='%s', enabled='%s')>" % (self.id, self.name, self.enabled)


class Project(Base, BaseDict):
    __tablename__ = "project"
    _attributes = ['id', 'name', 'extra', 'enabled', 'description', 'domain_id']

    id = Column(String(64), primary_key=True, nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, unique=True)
    extra = Column(Text)
    enabled = Column(SmallInteger)
    description = Column(Text)
    domain_id = Column(ForeignKey("domain.id"), nullable=False)

    user = relationship("User", backref="project")

    def __repr__(self):
        return "<Project(id='%s', name='%s', extra='%s', enabled='%s', \
                description='%s', domain_id=’%s’)>" % (
            self.id, self.name, self.extra, self.enabled, self.description,  self.domain_id)


class User(Base, BaseDict):
    __tablename__ = "user"
    _attributes = ['id', 'name', 'password', 'extra', 'enabled', 'project_id']

    id = Column(String(64), primary_key=True, nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, unique=True)
    password = Column(String(64), nullable=False)
    extra = Column(Text)
    enabled = Column(SmallInteger)
    project_id = Column(ForeignKey("project.id"), nullable=False)

    user_group_membership = relationship("UserGroupMembership", backref="user", cascade="all")
    user_role_membership = relationship("UserRoleMembership", backref="user", cascade="all")

    def __repr__(self):
        return "<User(id='%s', name='%s', project_id='%s', extra='%s', enabled='%s')>" % (
                   self.id, self.name, self.project_id, self.extra, self.enabled)


class Group(Base, BaseDict):
    __tablename__ = "group"
    _attributes = ['id', 'name', 'domain_id', 'extra', 'description']

    id = Column(String(36), primary_key=True, nullable=False, index=True)
    name = Column(String(45), nullable=False, index=True, unique=True)
    domain_id = Column(ForeignKey("domain.id"), nullable=False)
    extra = Column(Text)
    description = Column(Text)

    user_group_membership = relationship("UserGroupMembership", backref="group", cascade="all")
    group_role_membership = relationship("GroupRoleMembership", backref="group", cascade="all")

    def __repr__(self):
        return "<Group(id='%s', name='%s', domain_id='%s', extra='%s', description='%s')>" % (
                             self.id, self.name, self.domain_id, self.extra, self.description)


class Role(Base, BaseDict):
    __tablename__ = "role"
    _attributes = ['id', 'name', 'extra', 'description']

    id = Column(String(36), primary_key=True, nullable=False, index=True)
    name = Column(String(45), nullable=False, index=True, unique=True)
    extra = Column(Text)
    description = Column(Text)

    user_role_membership = relationship("UserRoleMembership", backref="role", cascade="all")
    group_role_membership = relationship("GroupRoleMembership", backref="role", cascade="all")

    def __repr__(self):
        return "<Role(id='%s', name='%s', extra='%s', description='%s')>" % (
                  self.id, self.name, self.extra, self.description)


class UserGroupMembership(Base, BaseDict):
    __tablename__ = "user_group_membership"

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    group_id = Column(ForeignKey("group.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    def __repr__(self):
        return "<User_group_membership(user_id='%s', group_id='%s')>" % (self.user_id, self.group_id)


class UserRoleMembership(Base, BaseDict):
    __tablename__ = "user_role_membership"

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    role_id = Column(ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    def __repr__(self):
        return "<User_group_membership(user_id='%s', role_id='%s')>" % (self.user_id, self.role_id)


class GroupRoleMembership(Base, BaseDict):
    __tablename__ = "group_role__membership"

    group_id = Column(ForeignKey("group.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    role_id = Column(ForeignKey("role.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    def __repr__(self):
        return "<User_group_membership(group_id='%s', role_id='%s')>" % (self.group_id, self.role_id)
