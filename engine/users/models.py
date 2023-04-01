from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class Organization(Base):
    __tablename__ = "Organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    email = Column(String, unique=True)
    users = relationship("User", back_populates="organization")


class Role(Base):
    __tablename__ = "Roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, index=True)
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("Roles.id"))
    organization_id = Column(Integer, ForeignKey("Organizations.id"))
