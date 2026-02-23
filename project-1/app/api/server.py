from fastapi import FastAPI, HTTPException

from app.services.users_service import UsersService
from app.services.exercises_service import ExercisesService
from app.services.workouts_service import WorkoutsService

app = FastAPI(title="Workout Tracker Service")

users_service = UsersService()
exercises_service = ExercisesService()
workouts_service = WorkoutsService()


@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------
# USERS (service layer)
# -------------------

@app.post("/users")
def create_user(first_name: str, last_name: str, email: str):
    try:
        return users_service.create_user(first_name, last_name, email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = users_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users")
def list_users(limit: int = 50):
    return users_service.list_users(limit=limit)


@app.put("/users/{user_id}/email")
def update_user_email(user_id: int, new_email: str):
    try:
        user = users_service.update_user_email(user_id, new_email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    return users_service.delete_user(user_id)


# ----------------------
# EXERCISES (service layer)
# ----------------------

@app.get("/exercises")
def list_exercises(limit: int = 100):
    return exercises_service.list_exercises(limit=limit)


@app.get("/exercises/{exercise_id}")
def get_exercise(exercise_id: int):
    ex = exercises_service.get_exercise(exercise_id)
    if ex is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ex


@app.post("/exercises")
def create_exercise(name: str, muscle_group: str, equipment: str):
    try:
        return exercises_service.create_exercise(name, muscle_group, equipment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/exercises/{exercise_id}")
def update_exercise(exercise_id: int, name: str, muscle_group: str, equipment: str):
    try:
        ex = exercises_service.update_exercise(exercise_id, name, muscle_group, equipment)
        if ex is None:
            raise HTTPException(status_code=404, detail="Exercise not found")
        return ex
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    return exercises_service.delete_exercise(exercise_id)


# ---------------------
# WORKOUTS (service layer)
# ---------------------

@app.get("/workouts")
def list_workouts(limit: int = 100):
    return workouts_service.list_workouts(limit=limit)


@app.get("/users/{user_id}/workouts")
def list_workouts_by_user(user_id: int, limit: int = 50):
    return workouts_service.list_workouts_by_user(user_id, limit=limit)


@app.get("/workouts/{workout_id}")
def get_workout(workout_id: int):
    w = workouts_service.get_workout(workout_id)
    if w is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return w


@app.post("/workouts")
def create_workout(user_id: int, workout_date: str, name: str, notes: str = ""):
    try:
        return workouts_service.create_workout(user_id, workout_date, name, notes)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/workouts/{workout_id}")
def update_workout(workout_id: int, workout_date: str, name: str, notes: str = ""):
    try:
        w = workouts_service.update_workout(workout_id, workout_date, name, notes)
        if w is None:
            raise HTTPException(status_code=404, detail="Workout not found")
        return w
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int):
    return workouts_service.delete_workout(workout_id)


"""
HOSTING NOTE (Render example):
- Create a new Web Service connected to your GitHub repo.
- Build command:
    pip install -r requirements.txt
- Start command:
    uvicorn app.api.server:app --host 0.0.0.0 --port 10000
- Render sets PORT automatically sometimes; if needed you can use --port $PORT
  (Render docs vary by template). If your instance provides $PORT, use:
    uvicorn app.api.server:app --host 0.0.0.0 --port $PORT
"""