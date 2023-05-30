-- Знайти список курсів, які відвідує студент.
SELECT students.name, subjects.name
FROM students
JOIN grades on students.id = grades.student_id
JOIN subjects on subjects.id = grades.subject_id
WHERE students.name = 'Kendra Leonard'
GROUP BY students.name, subjects.name