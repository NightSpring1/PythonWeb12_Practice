import db_students as db
from sqlalchemy import func, desc
from prettytable import PrettyTable


def my_select_01(session):
    """1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    a = session.query(db.Student.name, func.round(func.avg(db.Grade.grade_value), 2).label('avg_grade')) \
        .select_from(db.Grade) \
        .join(db.Student) \
        .group_by(db.Student.id) \
        .order_by(desc('avg_grade')) \
        .limit(5).all()
    return a


def my_select_02(session, subject_name):
    """2. Знайти студента із найвищим середнім балом з певного предмета."""
    a = session.query(db.Student.id,
                      db.Student.name,
                      func.round(func.avg(db.Grade.grade_value), 2).label('avg_grade')) \
        .select_from(db.Student) \
        .join(db.Grade) \
        .join(db.Subject) \
        .where(db.Subject.name == subject_name) \
        .group_by(db.Student.id) \
        .order_by(desc('avg_grade')) \
        .first()
    return a


def my_select_03(session):
    """3. Знайти середній бал у групах з певного предмета."""

    a = session.query(db.Group.name,
                      db.Subject.name,
                      func.round(func.avg(db.Grade.grade_value), 2).label('avg_grade')) \
        .select_from(db.Group) \
        .join(db.Student) \
        .join(db.Grade) \
        .join(db.Subject) \
        .group_by(db.Group.name, db.Subject.name) \
        .order_by(db.Group.name) \
        .all()
    return a


def my_select_04(session, group_name):
    """4. Знайти середній бал на потоці (по всій таблиці оцінок)."""
    a = session.query(db.Group.name,
                      func.round(func.avg(db.Grade.grade_value), 2).label('avg_grade')) \
        .select_from(db.Group) \
        .join(db.Student) \
        .join(db.Grade) \
        .where(db.Group.name == group_name) \
        .group_by(db.Group.name) \
        .all()
    return a


def my_select_05(session, teacher_name):
    """5. Знайти які курси читає певний викладач."""
    a = session.query(db.Teacher.name,
                      db.Subject.name) \
        .select_from(db.Subject) \
        .join(db.Teacher) \
        .where(db.Teacher.name == teacher_name) \
        .all()
    return a


def my_select_06(session, group_name):
    """6. Знайти список студентів у певній групі."""
    a = session.query(db.Group.name,
                      db.Student.name) \
        .select_from(db.Group) \
        .join(db.Student) \
        .where(db.Group.name == group_name) \
        .all()
    return a


def my_select_07(session, group_name, subject_name):
    """7. Знайти оцінки студентів у окремій групі з певного предмета."""
    a = session.query(db.Grade.grade_value,
                      db.Student.name,
                      db.Subject.name,
                      db.Group.name) \
        .select_from(db.Grade) \
        .join(db.Student) \
        .join(db.Subject) \
        .join(db.Group) \
        .where(db.Group.name == group_name, db.Subject.name == subject_name) \
        .all()
    return a


def my_select_08(session, teacher_name):
    """8. Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    a = session.query(db.Teacher.name,
                      db.Subject.name,
                      func.round(func.avg(db.Grade.grade_value), 2).label('avg_grade')) \
        .select_from(db.Teacher) \
        .join(db.Subject) \
        .join(db.Grade) \
        .where(db.Teacher.name == teacher_name) \
        .group_by(db.Teacher.name, db.Subject.name) \
        .all()
    return a


def my_select_09(session, student_name):
    """9. Знайти список курсів, які відвідує студент."""
    a = session.query(db.Student.name, db.Subject.name) \
        .select_from(db.Student) \
        .join(db.Grade) \
        .join(db.Subject) \
        .where(db.Student.name == student_name) \
        .group_by(db.Student.name, db.Subject.name) \
        .all()
    return a


def my_select_10(session, student_name, teacher_name):
    """10. Список курсів, які певному студенту читає певний викладач."""
    a = session.query(db.Subject.name, db.Teacher.name, db.Student.name) \
        .select_from(db.Subject) \
        .join(db.Teacher) \
        .join(db.Grade) \
        .join(db.Student) \
        .where(db.Student.name == student_name, db.Teacher.name == teacher_name) \
        .order_by(db.Subject.name) \
        .all()
    return a


def my_select_11(session, student_name, teacher_name):
    """11. Середній бал, який певний викладач ставить певному студентові."""
    a = session.query(db.Teacher.name,
                      db.Student.name,
                      func.round(func.avg(db.Grade.grade_value), 2).label('avg_grade')) \
        .select_from(db.Grade) \
        .join(db.Student) \
        .join(db.Subject) \
        .join(db.Teacher) \
        .where(db.Student.name == student_name, db.Teacher.name == teacher_name) \
        .group_by(db.Student.name, db.Teacher.name) \
        .all()
    return a


def my_select_12(session, group_name, subject_name):
    """12. Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    subq = session.query(func.max(db.Grade.date)) \
        .join(db.Subject) \
        .join(db.Student) \
        .filter(db.Grade.subject_id == db.Subject.id, db.Grade.student_id == db.Student.id) \
        .scalar_subquery()

    a = session.query(db.Student.name, db.Grade.grade_value, db.Grade.date) \
        .select_from(db.Student) \
        .join(db.Grade) \
        .join(db.Subject) \
        .join(db.Group) \
        .where(db.Group.name == group_name, db.Subject.name == subject_name, db.Grade.date == subq) \
        .all()
    return a


if __name__ == '__main__':
    with db.Session() as s:

        table = PrettyTable()

        table.add_rows(my_select_01(s))
        print(my_select_01.__doc__)
        print(table)
        table.clear()

        table.add_rows([my_select_02(s, subject_name='Physical Education')])
        print(my_select_02.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_03(s))
        print(my_select_03.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_04(s, group_name='P-177'))
        print(my_select_04.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_05(s, teacher_name='Karen Williams Jr.'))
        print(my_select_05.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_06(s, group_name='P-177'))
        print(my_select_06.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_07(s, group_name='Q-142', subject_name='Science'))
        print(my_select_07.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_08(s, teacher_name='Matthew Arnold PhD'))
        print(my_select_08.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_09(s, student_name='Brian Mitchell'))
        print(my_select_09.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_10(s, student_name='Troy Freeman', teacher_name='Anthony Curry MD'))
        print(my_select_10.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_11(s, student_name='Kristopher Rodriguez', teacher_name='Megan Hamilton DDS'))
        print(my_select_11.__doc__)
        print(table)
        table.clear()

        table.add_rows(my_select_12(s, group_name='C-139', subject_name='English Language'))
        print(my_select_12.__doc__)
        print(table)
        table.clear()
