-- 02_seed_data.sql (PostgreSQL)
-- Safe to re-run: clears existing rows first
TRUNCATE TABLE
  sets,
  workout_exercises,
  workouts,
  exercises,
  users
RESTART IDENTITY CASCADE;

-- USERS (10 rows)
INSERT INTO users (first_name, last_name, email)
SELECT
  'User' || gs,
  'Test' || gs,
  'user' || gs || '@example.com'
FROM generate_series(1,10) gs;

-- EXERCISES (15 rows)
INSERT INTO exercises (name, muscle_group, equipment) VALUES
('Bench Press', 'Chest', 'Barbell'),
('Incline DB Press', 'Chest', 'Dumbbell'),
('Push-Up', 'Chest', 'Bodyweight'),
('Pull-Up', 'Back', 'Bodyweight'),
('Lat Pulldown', 'Back', 'Machine'),
('Barbell Row', 'Back', 'Barbell'),
('Bicep Curl', 'Arms', 'Dumbbell'),
('Tricep Pushdown', 'Arms', 'Cable'),
('Shoulder Press', 'Shoulders', 'Dumbbell'),
('Lateral Raise', 'Shoulders', 'Dumbbell'),
('Squat', 'Legs', 'Barbell'),
('Leg Press', 'Legs', 'Machine'),
('Deadlift', 'Legs', 'Barbell'),
('Calf Raise', 'Legs', 'Machine'),
('Plank', 'Core', 'Bodyweight');

-- WORKOUTS (30 rows target; insert is conflict-safe)
-- 3 workouts per user for 10 users, dates spread across 10 days
INSERT INTO workouts (user_id, workout_date, name, notes)
SELECT
  u.user_id,
  (CURRENT_DATE - (u.user_id % 10))::date,
  CASE (u.user_id % 3)
    WHEN 0 THEN 'Push Day'
    WHEN 1 THEN 'Pull Day'
    ELSE 'Leg Day'
  END,
  'Auto-generated workout'
FROM users u
CROSS JOIN generate_series(1,3) w
ORDER BY u.user_id
ON CONFLICT (user_id, workout_date, name) DO NOTHING;

-- WORKOUT_EXERCISES (~60 rows)
-- Add 2 exercises to each workout (simple and deterministic)
INSERT INTO workout_exercises (workout_id, exercise_id, exercise_order)
SELECT
  w.workout_id,
  ((w.workout_id % 15) + 1) AS exercise_id,
  1
FROM workouts w;

INSERT INTO workout_exercises (workout_id, exercise_id, exercise_order)
SELECT
  w.workout_id,
  (((w.workout_id + 5) % 15) + 1) AS exercise_id,
  2
FROM workouts w
WHERE ((w.workout_id % 15) + 1) <> (((w.workout_id + 5) % 15) + 1);

-- SETS (>= 180 rows)
-- 3 sets per workout_exercise
INSERT INTO sets (workout_exercise_id, set_number, reps, weight_lbs, is_pr)
SELECT
  we.workout_exercise_id,
  s.set_number,
  (8 + (we.workout_exercise_id % 5)) AS reps,
  (95 + (we.workout_exercise_id % 20) * 5)::numeric AS weight_lbs,
  (s.set_number = 3 AND we.workout_exercise_id % 10 = 0) AS is_pr
FROM workout_exercises we
CROSS JOIN (VALUES (1), (2), (3)) AS s(set_number);

-- Optional: quick proof query (run separately if you want)
-- SELECT 'users' table_name, COUNT(*) FROM users
-- UNION ALL SELECT 'exercises', COUNT(*) FROM exercises
-- UNION ALL SELECT 'workouts', COUNT(*) FROM workouts
-- UNION ALL SELECT 'workout_exercises', COUNT(*) FROM workout_exercises
-- UNION ALL SELECT 'sets', COUNT(*) FROM sets;
