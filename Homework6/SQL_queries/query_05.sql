--Знайти які курси читає певний викладач.
SELECT teachers.name, subjects.name
FROM subjects
JOIN teachers on subjects.teacher_id = teachers.id
WHERE teachers.name = 'Patricia Arias MD';