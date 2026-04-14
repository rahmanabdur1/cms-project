from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent")
    contents = relationship("Content", back_populates="category")


class Content(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    slug = Column(String(255), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    category = relationship("Category", back_populates="contents")
    interactions = relationship(
        "Interaction",
        back_populates="content",
        cascade="all, delete"
    )


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"), nullable=False)
    keyword = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    url = Column(Text, nullable=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    content = relationship("Content", back_populates="interactions")