-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
SELECT students.name, round(avg(grades.grade_value), 1) AS avg_grade
FROM students
JOIN grades ON students.id = grades.student_id
GROUP BY students.name
ORDER BY avg_grade DESC
LIMIT 5;