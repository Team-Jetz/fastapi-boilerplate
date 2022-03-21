from settings.databases import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4, nullable=False)
    username =  Column(String, nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    is_active = Column(Boolean, server_default=expression.false(), nullable=False)
    is_admin = Column(Boolean, server_default=expression.false(), nullable=False)
    is_superuser = Column(Boolean, server_default=expression.false(), nullable=False)

    registered_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))

    posts = relationship('Post', back_populates='author')
