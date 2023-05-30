-- Середній бал, який певний викладач ставить певному студентові.
SELECT teachers.name, students.name, ROUND(AVG(grades.grade_value), 2) AS avg_grade
FROM grades
JOIN students ON students.id = grades.student_id
JOIN subjects ON subjects.id = grades.subject_id
JOIN teachers ON teachers.id = subjects.teacher_id
WHERE students.name = 'Maria Strickland'
AND teachers.name = 'Patricia Arias MD'
GROUP BY students.name, teachers.name