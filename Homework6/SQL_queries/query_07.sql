-- Знайти оцінки студентів у окремій групі з певного предмета.
SELECT grades.grade_value, students.name, subjects.name, groups.name
FROM grades
JOIN students ON students.id = grades.student_id
JOIN subjects ON subjects.id = grades.subject_id
JOIN groups ON groups.id = students.group_id
WHERE groups.name = 'Washington, Perez and Meyers'
AND subjects.name = 'Art'