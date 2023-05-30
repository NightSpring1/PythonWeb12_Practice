-- Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT students.name, grades.grade_value, grades.date
FROM students
JOIN grades on students.id = grades.student_id
JOIN subjects on subjects.id = grades.subject_id
JOIN groups on groups.id = students.group_id
WHERE groups.name = 'Garza, Smith and Dudley'
AND subjects.name = 'Mathematics'
AND grades.date = (SELECT MAX(date)
                   FROM grades
                   WHERE subject_id = subjects.id
                   AND students.id = grades.student_id);
