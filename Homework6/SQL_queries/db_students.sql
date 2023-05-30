CREATE TABLE IF NOT EXISTS groups (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30) NOT NULL,
  group_id INT,
  FOREIGN KEY (group_id) REFERENCES groups(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS teachers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(30) NOT NULL,
  teacher_id INT,
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS grades (
  id SERIAL PRIMARY KEY,
  student_id INT,
  subject_id INT,
  grade_value INT,
  date TIMESTAMP NOT NULL DEFAULT NOW(),
  FOREIGN KEY (student_id) REFERENCES students(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  FOREIGN KEY (subject_id) REFERENCES subjects(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE OR REPLACE PROCEDURE add_subject(
  IN subject_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO subjects(name) VALUES (subject_name);
END;
$$;


CREATE OR REPLACE PROCEDURE add_teacher(
  IN teacher_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO teachers(name) VALUES (teacher_name);
END;
$$;

CREATE OR REPLACE PROCEDURE add_group(
  IN group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO groups(name) VALUES (group_name);
END;
$$;

CREATE OR REPLACE PROCEDURE add_student(
  IN student_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO students(name) VALUES (student_name);
END;
$$;

CREATE OR REPLACE PROCEDURE set_subject_teacher(
  IN subject_name VARCHAR,
  IN teacher_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE subjects
    SET teacher_id = teachers.id
    FROM teachers
    WHERE subjects.name = subject_name
    AND teachers.name = teacher_name;
END;
$$;

CREATE OR REPLACE PROCEDURE set_student_group(
  IN student_name VARCHAR,
  IN group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE students
    SET group_id = groups.id
    FROM groups
    WHERE students.name = student_name
    AND groups.name = group_name;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_grade(
  IN student_name VARCHAR,
  IN subject_name VARCHAR,
  IN grade INTEGER,
  IN date_acquired TIMESTAMP
)
LANGUAGE plpgsql
AS $$
DECLARE
    stud_id INTEGER;
    subj_id INTEGER;
BEGIN
  SELECT id INTO stud_id
  FROM students
  WHERE name = student_name;

  SELECT id INTO subj_id
  FROM subjects
  WHERE name = subject_name;

  INSERT INTO grades (student_id, subject_id, grade_value, date)
  VALUES (stud_id, subj_id, grade, date_acquired);
END;
$$;