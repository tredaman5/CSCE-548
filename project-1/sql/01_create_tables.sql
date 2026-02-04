-- 01_create_tables.sql (PostgreSQL)

DROP TABLE IF EXISTS sets;
DROP TABLE IF EXISTS workout_exercises;
DROP TABLE IF EXISTS workouts;
DROP TABLE IF EXISTS exercises;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id      SERIAL PRIMARY KEY,
  first_name   VARCHAR(50)  NOT NULL,
  last_name    VARCHAR(50)  NOT NULL,
  email        VARCHAR(255) NOT NULL UNIQUE,
  created_at   TIMESTAMP    NOT NULL DEFAULT NOW(),
  CHECK (position('@' in email) > 1)
);

CREATE TABLE workouts (
  workout_id   SERIAL PRIMARY KEY,
  user_id      INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  workout_date DATE NOT NULL,
  name         VARCHAR(100) NOT NULL,
  notes        TEXT,
  created_at   TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, workout_date, name)
);

CREATE TABLE exercises (
  exercise_id  SERIAL PRIMARY KEY,
  name         VARCHAR(100) NOT NULL UNIQUE,
  muscle_group VARCHAR(50)  NOT NULL,
  equipment    VARCHAR(50)  NOT NULL,
  CHECK (char_length(name) >= 2)
);

-- Join table: a workout contains multiple exercises
CREATE TABLE workout_exercises (
  workout_exercise_id SERIAL PRIMARY KEY,
  workout_id          INT NOT NULL REFERENCES workouts(workout_id) ON DELETE CASCADE,
  exercise_id         INT NOT NULL REFERENCES exercises(exercise_id) ON DELETE RESTRICT,
  exercise_order      INT NOT NULL,
  UNIQUE (workout_id, exercise_id),
  CHECK (exercise_order >= 1)
);

-- Each workout_exercise can have multiple sets
CREATE TABLE sets (
  set_id               SERIAL PRIMARY KEY,
  workout_exercise_id  INT NOT NULL REFERENCES workout_exercises(workout_exercise_id) ON DELETE CASCADE,
  set_number           INT NOT NULL,
  reps                 INT NOT NULL,
  weight_lbs           NUMERIC(6,2) NOT NULL,
  is_pr                BOOLEAN NOT NULL DEFAULT FALSE,
  CHECK (set_number >= 1),
  CHECK (reps >= 1 AND reps <= 100),
  CHECK (weight_lbs >= 0 AND weight_lbs <= 2000)
);

-- Helpful indexes for retrieval speed
CREATE INDEX idx_workouts_user_date ON workouts(user_id, workout_date);
CREATE INDEX idx_wex_workout ON workout_exercises(workout_id);
CREATE INDEX idx_sets_wex ON sets(workout_exercise_id);
