import db_students as db
from argparse import ArgumentParser
from prettytable import PrettyTable


def parser_init() -> ArgumentParser:
    parser = ArgumentParser(description="Command Parser", epilog="End.", exit_on_error=False, add_help=True)
    parser.add_argument('-a', "--action",
                        choices=['create', 'read', 'update', 'delete'],
                        help="Action to execute",
                        required=True)
    parser.add_argument('-m', "--model",
                        choices=['Group', 'Teacher', 'Student', 'Subject', 'Grade'],
                        help="Model on which to do action.")
    parser.add_argument('-id', "--identification", type=int, help="Id of record to change.")
    parser.add_argument('-n', "--name", type=str, help="Name entry.", nargs="*")

    return parser


def create_group(session, **kwargs) -> str:
    if not kwargs['name']:
        return "Nothing Happened."
    session.add(db.Group(name=kwargs['name']))
    return f'Group {kwargs["name"]} added to db.'


def create_teacher(session, **kwargs) -> str:
    if not kwargs['name']:
        return "Nothing Happened."
    session.add(db.Teacher(name=kwargs['name']))
    return f'Teacher {kwargs["name"]} added to db.'


def create_student(session, **kwargs) -> str:
    if not kwargs['name']:
        return "Nothing Happened."
    session.add(db.Student(name=kwargs['name']))
    return f'Student {kwargs["name"]} added to db.'


def create_subject(session, **kwargs) -> str:
    if not kwargs['name']:
        return "Nothing Happened."
    session.add(db.Subject(name=kwargs['name']))
    return f'Subject {kwargs["name"]} added to db.'


def create_grade(session, **kwargs) -> str:
    raise NotImplementedError


def read_group(session, **kwargs) -> str:
    groups = session.query(db.Group.id, db.Group.name).all()
    table = PrettyTable()
    table.field_names = ["ID", "Name"]
    for group in groups:
        table.add_row((group.id, group.name))
    return str(table)


def read_teacher(session, **kwargs) -> str:
    teachers = session.query(db.Teacher.id, db.Teacher.name).all()
    table = PrettyTable()
    table.field_names = ["ID", "Name"]
    for teacher in teachers:
        table.add_row((teacher.id, teacher.name))
    return str(table)


def read_student(session, **kwargs) -> str:
    students = session.query(db.Student.id, db.Student.name).all()
    table = PrettyTable()
    table.field_names = ["ID", "Name"]
    for student in students:
        table.add_row((student.id, student.name))
    return str(table)


def read_subject(session, **kwargs) -> str:
    subjects = session.query(db.Subject.id, db.Subject.name).all()
    table = PrettyTable()
    table.field_names = ["ID", "Name"]
    for subject in subjects:
        table.add_row((subject.id, subject.name))
    return str(table)


def read_grade(session, **kwargs) -> str:
    raise NotImplementedError


def update_group(session, **kwargs) -> str:
    if not kwargs['ident'] or not kwargs['name']:
        return "Nothing Happened."
    group = session.get(db.Group, kwargs['ident'])
    group.name = kwargs['name']
    session.add(group)
    return f'Group with id {kwargs["ident"]} changed to {kwargs["name"]}'


def update_teacher(session, **kwargs) -> str:
    if not kwargs['ident'] or not kwargs['name']:
        return "Nothing Happened."
    teacher = session.get(db.Teacher, kwargs['ident'])
    teacher.name = kwargs['name']
    session.add(teacher)
    return f'Teacher with id {kwargs["ident"]} changed to {kwargs["name"]}'


def update_student(session, **kwargs) -> str:
    if not kwargs['ident'] or not kwargs['name']:
        return "Nothing Happened."
    student = session.get(db.Student, kwargs['ident'])
    student.name = kwargs['name']
    session.add(student)
    return f'Student with id {kwargs["ident"]} changed to {kwargs["name"]}'


def update_subject(session, **kwargs) -> str:
    if not kwargs['ident'] or not kwargs['name']:
        return "Nothing Happened."
    subject = session.get(db.Subject, kwargs['ident'])
    subject.name = kwargs['name']
    session.add(subject)
    return f'Subject with id {kwargs["ident"]} changed to {kwargs["name"]}'


def update_grade(session, **kwargs) -> str:
    raise NotImplementedError


def delete_group(session, **kwargs) -> str:
    if not kwargs['ident']:
        return "Nothing Happened."
    group = session.get(db.Group, kwargs['ident'])
    session.delete(group)
    return f'Group with {kwargs["ident"]} was removed from db.'


def delete_teacher(session, **kwargs) -> str:
    if not kwargs['ident']:
        return "Nothing Happened."
    teacher = session.get(db.Teacher, kwargs['ident'])
    session.delete(teacher)
    return f'Teacher with {kwargs["ident"]} was removed from db.'


def delete_student(session, **kwargs) -> str:
    if not kwargs['ident']:
        return "Nothing Happened."
    student = session.get(db.Teacher, kwargs['ident'])
    session.delete(student)
    return f'Student with {kwargs["ident"]} was removed from db.'


def delete_subject(session, **kwargs) -> str:
    if not kwargs['ident']:
        return "Nothing Happened."
    subject = session.get(db.Teacher, kwargs['ident'])
    session.delete(subject)
    return f'Subject with {kwargs["ident"]} was removed from db.'


def delete_grade(session, **kwargs) -> str:
    raise NotImplementedError


action = {('create', 'Group'): create_group,
          ('create', 'Teacher'): create_teacher,
          ('create', 'Student'): create_student,
          ('create', 'Subject'): create_subject,
          ('create', 'Grade'): create_grade,
          ('read', 'Group'): read_group,
          ('read', 'Teacher'): read_teacher,
          ('read', 'Student'): read_student,
          ('read', 'Subject'): read_subject,
          ('read', 'Grade'): read_grade,
          ('update', 'Group'): update_group,
          ('update', 'Teacher'): update_teacher,
          ('update', 'Student'): update_student,
          ('update', 'Subject'): update_subject,
          ('update', 'Grade'): update_grade,
          ('delete', 'Group'): delete_group,
          ('delete', 'Teacher'): delete_teacher,
          ('delete', 'Student'): delete_student,
          ('delete', 'Subject'): delete_subject,
          ('delete', 'Grade'): delete_grade,
          }

if __name__ == "__main__":
    p = parser_init()
    arg = p.parse_args()
    command = (arg.action, arg.model)

    with db.Session() as s:
        try:
            respond = action[command](s, ident=arg.identification, name=' '.join(arg.name) if arg.name else None)
            s.commit()
        except Exception:
            respond = "Nothing Happened. Or id was not found, or another Exception was raised."
    print(respond)
