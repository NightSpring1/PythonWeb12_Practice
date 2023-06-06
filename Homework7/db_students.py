from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Group(Base):
    __tablename__: str = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='SET NULL', onupdate='CASCADE'))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__: str = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='SET NULL', onupdate='CASCADE'))
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='SET NULL', onupdate='CASCADE'))
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='SET NULL', onupdate='CASCADE'))
    grade_value = Column(Integer)
    date = Column(TIMESTAMP, nullable=False, default=func.now())
    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')


mysql = 'mysql+pymysql://root:29an99fr@192.168.1.242:3306/students'
postgres = 'postgresql://postgres:29an99fr@192.168.1.242:5432/postgres'
mssql = 'mssql+pyodbc://sa:29aN99fR@192.168.1.40:1433/students?driver=ODBC+Driver+18+for+SQL+Server'
sqlite = 'sqlite:///students.db'

engine = create_engine(postgres)
# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()




