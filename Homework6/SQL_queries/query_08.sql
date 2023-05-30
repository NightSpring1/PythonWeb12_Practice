-- Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT teachers.name, subjects.name , round(avg(grades.grade_value),1) as avg_grade
FROM teachers
JOIN subjects on teachers.id = subjects.teacher_id
JOIN grades on subjects.id = grades.subject_id
WHERE teachers.name = 'Patricia Arias MD'
GROUP BY teachers.name, subjects.name