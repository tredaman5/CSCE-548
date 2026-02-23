from app.repositories.workouts_repo import WorkoutsRepo


class WorkoutsService:
    """
    Business layer for Workouts.
    Exposes all CRUD methods in WorkoutsRepo:
      - list_all(limit)
      - list_by_user(user_id, limit)
      - get_by_id(workout_id)
      - create(user_id, workout_date, name, notes)
      - update(workout_id, workout_date, name, notes)
      - delete(workout_id)
    """

    def __init__(self):
        self.repo = WorkoutsRepo()

    def list_workouts(self, limit: int = 100):
        return self.repo.list_all(limit=limit)

    def list_workouts_by_user(self, user_id: int, limit: int = 50):
        return self.repo.list_by_user(user_id, limit=limit)

    def get_workout(self, workout_id: int):
        return self.repo.get_by_id(workout_id)

    def create_workout(self, user_id: int, workout_date: str, name: str, notes: str = ""):
        name = (name or "").strip()
        notes = "" if notes is None else notes

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("user_id must be a positive integer")
        if not workout_date:
            raise ValueError("workout_date is required (YYYY-MM-DD)")
        if len(name) < 2:
            raise ValueError("name must be at least 2 characters")

        return self.repo.create(user_id, workout_date, name, notes)

    def update_workout(self, workout_id: int, workout_date: str, name: str, notes: str = ""):
        name = (name or "").strip()
        notes = "" if notes is None else notes

        if not workout_date:
            raise ValueError("workout_date is required (YYYY-MM-DD)")
        if len(name) < 2:
            raise ValueError("name must be at least 2 characters")

        return self.repo.update(workout_id, workout_date, name, notes)

    def delete_workout(self, workout_id: int):
        return {"deleted": self.repo.delete(workout_id)}