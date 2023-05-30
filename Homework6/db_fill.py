import faker
from random import randint, choice
import psycopg2

NUMBER_STUDENTS = 20
NUMBER_TEACHERS = 8
NUMBER_GROUPS = 5
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


def gen_fake_data(n_students, n_teachers, n_groups):
    students = []
    teachers = []
    groups = []

    for _ in range(n_students):
        students.append(fake.name())
    for _ in range(n_teachers):
        teachers.append(fake.name() + " " + fake.suffix())
    for _ in range(n_groups):
        groups.append(fake.company())

    return students, teachers, groups


def fill_db(students, teachers, groups):
    with psycopg2.connect(host="192.168.1.242",
                          port="5432",
                          user="postgres",
                          password="29an99fr") as db:
        cursor = db.cursor()

        # Fill subjects
        data = [(subject,) for subject in SUBJECTS]
        cursor.executemany("CALL add_subject(%s)", data)

        # Fill teachers
        data = [(teacher,) for teacher in teachers]
        cursor.executemany("CALL add_teacher(%s)", data)

        # Fill groups
        data = [(group,) for group in groups]
        cursor.executemany("CALL add_group(%s)", data)

        # Fill students
        data = [(student,) for student in students]
        cursor.executemany("CALL add_student(%s)", data)

        # Assign teacher for each subject
        data = [(subj, choice(teachers)) for subj in SUBJECTS]
        cursor.executemany("CALL set_subject_teacher(%s, %s)", data)

        # Assign group for each student
        data = [(stud, choice(groups)) for stud in students]
        cursor.executemany("CALL set_student_group(%s, %s)", data)

        # Insert random marks in randon subject for random student
        data = [(choice(students), choice(SUBJECTS), randint(1, 12), fake.date_this_month()) for _ in range(100)]
        cursor.executemany('CALL insert_grade(%s, %s, %s, %s)', data)


if __name__ == "__main__":
    fill_db(*gen_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS, NUMBER_GROUPS))
