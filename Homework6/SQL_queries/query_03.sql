-- Знайти середній бал у групах з певного предмета.
SELECT groups.name, subjects.name, round(AVG(grades.grade_value), 1) AS avg_grade
FROM groups
JOIN students ON groups.id = students.group_id
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
GROUP BY groups.name, subjects.name
ORDER BY groups.name;