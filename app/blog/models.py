from email.policy import default
from settings.databases import Base
from sqlalchemy import Column, Text, String, Boolean
from sqlalchemy.sql import expression
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4

class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    title =  Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default=expression.true(), nullable=False)
    image_url = Column(String(255), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))

    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    author = relationship('User', back_populates='posts')


class Votes(Base):
    __tablename__ = 'votes'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
