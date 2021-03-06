from enum import unique
from settings.databases import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4


class User(Base):
    __tablename__ = 'users'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid4, nullable=False)
    username =  Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    is_active = Column(Boolean, server_default=expression.false(), nullable=False)
    is_admin = Column(Boolean, server_default=expression.false(), nullable=False)
    is_superuser = Column(Boolean, server_default=expression.false(), nullable=False)

    registered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))

    posts = relationship('Post', back_populates='author')


class PasswordReset(Base):
    __tablename__ = 'password_resets'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid4, nullable=False)
    email = Column(String(255), index=True, nullable=False)
    reset_code = Column(UUIDType(binary=False), index=True, nullable=False)

    expires_in = Column(TIMESTAMP(timezone=True), nullable=False)
    is_expired = Column(Boolean, server_default=expression.false(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))


class ActivationToken(Base):
    __tablename__ = 'activation_tokens'

    id = Column(UUIDType(binary=False), primary_key=True, index=True, default=uuid4, nullable=False)
    email = Column(String(255), index=True, nullable=False)
    activation_code = Column(UUIDType(binary=False), index=True, nullable=False)

    expires_in = Column(TIMESTAMP(timezone=True), nullable=False)
    is_expired = Column(Boolean, server_default=expression.false(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))


class BlackListedToken(Base):
    __tablename__ = 'black_listed_tokens'

    user_id = Column(UUIDType(binary=False), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    access_token = Column(String(255), unique=True)
