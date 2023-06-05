import faker
import string
from random import randint, choice
import db_students as db
from sqlalchemy import func, desc
import psycopg2

NUMBER_STUDENTS = 20
NUMBER_TEACHERS = 8
NUMBER_GROUPS = 10
SUBJECTS = [
    "Mathematics",
    "English Language",
    "Science",
    "History",
    "Geography",
    "Physical Education",
    "Art",
    "Music",
    "Computer Science",
    "Foreign Language",
]

fake = faker.Faker()


def generate_fake_students(n_students):
    students_names = []
    for _ in range(n_students):
        students_names.append(fake.name())
    return students_names


def generate_fake_teachers(n_teachers):
    teachers_names = []
    for _ in range(n_teachers):
        teachers_names.append(fake.name() + " " + fake.suffix())
    return teachers_names


def generate_fake_groups(n_groups):
    groups_names = []
    for _ in range(n_groups):
        groups_names.append(choice(string.ascii_uppercase) + '-' + str(randint(100, 200)))
    return groups_names


if __name__ == "__main__":
    with db.Session() as session:
        groups = list()
        for group_name in generate_fake_groups(NUMBER_GROUPS):
            groups.append(db.Group(name=group_name))
        session.add_all(groups)
        session.commit()

        teachers = list()
        for teacher_name in generate_fake_teachers(NUMBER_TEACHERS):
            teachers.append(db.Teacher(name=teacher_name))
        session.add_all(teachers)
        session.commit()

        students = list()
        for student_name in generate_fake_students(NUMBER_STUDENTS):
            group = choice(groups)
            students.append(db.Student(name=student_name, group_id=group.id))
        session.add_all(students)
        session.commit()

        subjects = list()
        for subject_name in SUBJECTS:
            teacher = choice(teachers)
            subjects.append(db.Subject(name=subject_name, teacher_id=teacher.id))
        session.add_all(subjects)
        session.commit()

        grades = list()
        for _ in range(600):
            subject = choice(subjects)
            student = choice(students)
            grade = randint(1, 12)
            date = fake.date_this_month()
            grades.append(db.Grade(student_id=student.id, subject_id=subject.id, grade_value=grade, date=date))
        session.add_all(grades)
        session.commit()
