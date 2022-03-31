from email.policy import default
from settings.databases import Base
from sqlalchemy import Column, Text, String, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4, nullable=False)
    title =  Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default=expression.true(), nullable=False)
    image_url = Column(String(255), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))

    author_id = Column(UUIDType(binary=False), ForeignKey('users.id'), nullable=True)
    author = relationship('User', back_populates='posts')


class Votes(Base):
    __tablename__ = 'votes'

    user_id = Column(UUIDType(binary=False), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = Column(UUIDType(binary=False), ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
