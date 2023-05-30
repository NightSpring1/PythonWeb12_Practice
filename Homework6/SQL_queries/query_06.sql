-- Знайти список студентів у певній групі.
SELECT groups.name, students.name
FROM groups
JOIN students on groups.id = students.group_id
WHERE groups.name = 'Washington, Perez and Meyers';