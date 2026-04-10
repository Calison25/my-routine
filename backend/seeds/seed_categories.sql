INSERT INTO training_categories (id, name) VALUES
(1, 'Musculação'),
(2, 'Cardio'),
(3, 'Pilates')
ON CONFLICT (id) DO NOTHING;
