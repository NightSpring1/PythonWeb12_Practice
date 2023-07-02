from datetime import date
from sqlalchemy import Integer, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Phone(Base):
    __tablename__ = 'phones'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'))
    contact = relationship("Contact", back_populates="phones")


class Email(Base):
    __tablename__ = 'emails'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    contact_id: Mapped[int] = mapped_column(Integer, ForeignKey('contacts.id', ondelete='CASCADE'))
    contact = relationship("Contact", back_populates="emails")


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True, index=True)
    emails: Mapped[Email] = relationship("Email", back_populates="contact", lazy='joined', cascade="all, delete")
    phones: Mapped[Phone] = relationship("Phone", back_populates="contact", lazy='joined', cascade="all, delete")
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)




if __name__ == "__main__":
    pass
    # SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:29an99fr@192.168.1.242:5432/db_contacts"
    # engine = create_engine(SQLALCHEMY_DATABASE_URL)
    # Base.metadata.create_all(engine)
    # Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # session = Session()
    #
    # session.add(Contact(first_name='Alexander',
    #                     last_name='Singaevsky',
    #                     emails=[Email(address='deroy193@gmail.com'), Email(address='alexander.singaevsky@gmail.com')],
    #                     phones=[Phone(number='+380504105593'), Phone(number='+33769206871')],
    #                     birthday=date(year=1994, month=9, day=10),
    #                     description='Very good person'))
    # session.commit()
    # session.close()
    #
    # me = session.query(Contact).first()

