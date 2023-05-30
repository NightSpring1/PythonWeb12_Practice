-- Знайти студента із найвищим середнім балом з певного предмета.
SELECT students.id, students.name, AVG(grades.grade_value) AS avg_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.name = 'Physical Education'
GROUP BY students.id, students.name
ORDER BY avg_grade DESC
LIMIT 1;