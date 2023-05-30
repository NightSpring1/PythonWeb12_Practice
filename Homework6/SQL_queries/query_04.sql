-- Знайти середній бал на потоці (по всій таблиці оцінок).
SELECT groups.name, round(avg(g.grade_value),1) as avg_grade
FROM groups
JOIN students s on groups.id = s.group_id
JOIN grades g on s.id = g.student_id
WHERE groups.name = 'Watts Group'
GROUP BY groups.name;