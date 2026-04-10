INSERT INTO muscle_groups (id, name, category_id) VALUES
(1, 'Peito', 1),
(2, 'Costas', 1),
(3, 'Ombros', 1),
(4, 'Bíceps', 1),
(5, 'Tríceps', 1),
(6, 'Pernas', 1),
(7, 'Abdômen', 1)
ON CONFLICT (id) DO NOTHING;
