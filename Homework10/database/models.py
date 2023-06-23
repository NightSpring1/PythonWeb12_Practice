from sqlalchemy import Column, Integer, String, ForeignKey, TEXT, Table, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

quote_tag_association = Table(
    "note_tag_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("note", Integer, ForeignKey("quotes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)


class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='SET NULL', onupdate='CASCADE'))
    tags = relationship("Tag", secondary=quote_tag_association, backref="quotes")
    quote = Column(TEXT)
    authors = relationship("Author", back_populates="quotes")


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50), nullable=False)
    born_date = Column(String(50))
    born_location = Column(String(70))
    description = Column(TEXT)
    quotes = relationship("Quote", back_populates="authors")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    login = Column(String(40), nullable=False, unique=True)
    password = Column(String(40), nullable=False)
    is_active = Column(Boolean(), nullable=False, default=True)
    is_authenticated = Column(Boolean(), nullable=False, default=True)
    is_anonymous = Column(Boolean(), nullable=False, default=False)

    def get_id(self):
        return str(self.id)
