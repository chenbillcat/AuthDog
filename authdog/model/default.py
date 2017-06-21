# coding:utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict


class Domain(Base):
    __tablename__ = "domain"

    id = Column(String(64), primary_key=True, nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, unique=True)
    enabled = Column(SmallInteger)

    project = relationship("Project", backref="domain")
    group = relationship("Group", backref="domain")

    def __repr__(self):
        return "<Domain(id='%s', name='%s', enabled='%s')>" % (self.id, self.name, self.enabled)


class Project(Base):
    __tablename__ = "project"

    id = Column(String(64), primary_key=True, nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, unique=True)
    extra = Column(Text)
    enabled = Column(SmallInteger)
    description = Column(Text)
    domain_id = Column(ForeignKey("domain.id"))

    user = relationship("User", backref="project")

    def __repr__(self):
        return "<Project(id='%s', name='%s', extra='%s', enabled='%s', \
                description='%s', domain_id=’%s’)>" % (
            self.id, self.name, self.extra, self.enabled, self.description,  self.domain_id)


class User(Base):
    __tablename__ = "user"

    id = Column(String(64), primary_key=True, nullable=False, index=True)
    name = Column(String(64), nullable=False, index=True, unique=True)
    password = Column(String(64), nullable=False)
    extra = Column(Text)
    enabled = Column(SmallInteger)
    project_id = Column(ForeignKey("project.id"))

    user_group_membership = relationship("UserGroupMembership", backref="user")
    user_role_membership = relationship("UserRoleMembership", backref="user")

    def __repr__(self):
        return "<User(id='%s', name='%s', project_id='%s', extra='%s', enabled='%s')>" % (
                   self.id, self.name, self.project_id, self.extra, self.enabled)


class Group(Base):
    __tablename__ = "group"

    id = Column(String(36), primary_key=True, nullable=False, index=True)
    name = Column(String(45), nullable=False, index=True, unique=True)
    domain_id = Column(ForeignKey("domain.id"))
    extra = Column(Text)
    description = Column(Text)

    user_group_membership = relationship("UserGroupMembership", backref="group")
    group_role_membership = relationship("GroupRoleMembership", backref="group")

    def __repr__(self):
        return "<Group(id='%s', name='%s', domain_id='%s', extra='%s', description='%s')>" % (
                             self.id, self.name, self.domain_id, self.extra, self.description)


class Role(Base):
    __tablename__ = "role"

    id = Column(String(36), primary_key=True, nullable=False, index=True)
    name = Column(String(45), nullable=False, index=True, unique=True)
    extra = Column(Text)
    description = Column(Text)

    user_role_membership = relationship("UserRoleMembership", backref="role")
    group_role_membership = relationship("GroupRoleMembership", backref="role")

    def __repr__(self):
        return "<Role(id='%s', name='%s', extra='%s', description='%s')>" % (
                  self.id, self.name, self.extra, self.description)


class UserGroupMembership(Base):
    __tablename__ = "user_group_membership"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    group_id = Column(ForeignKey("group.id"), primary_key=True)

    def __repr__(self):
        return "<User_group_membership(user_id='%s', group_id='%s')>" % (self.user_id, self.group_id)


class UserRoleMembership(Base):
    __tablename__ = "user_role_membership"

    user_id = Column(ForeignKey("user.id"), primary_key=True)
    role_id = Column(ForeignKey("role.id"), primary_key=True)

    def __repr__(self):
        return "<User_group_membership(user_id='%s', role_id='%s')>" % (self.user_id, self.role_id)


class GroupRoleMembership(Base):
    __tablename__ = "group_role__membership"

    group_id = Column(ForeignKey("group.id"), primary_key=True)
    role_id = Column(ForeignKey("role.id"), primary_key=True)

    def __repr__(self):
        return "<User_group_membership(group_id='%s', role_id='%s')>" % (self.group_id, self.role_id)
