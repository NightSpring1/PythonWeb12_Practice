-- Список курсів, які певному студенту читає певний викладач.
SELECT subjects.name , teachers.name, students.name
FROM subjects
JOIN teachers on teachers.id = subjects.teacher_id
JOIN grades on subjects.id = grades.subject_id
JOIN students on students.id = grades.student_id
WHERE students.name = 'Maureen Goodwin'
AND teachers.name = 'Justin Rivers DDS'
ORDER BY subjects.name