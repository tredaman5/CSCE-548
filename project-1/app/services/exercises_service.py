from app.repositories.exercises_repo import ExercisesRepo


class ExercisesService:
    """
    Business layer for Exercises.
    Exposes all CRUD methods in ExercisesRepo:
      - list_all(limit)
      - get_by_id(exercise_id)
      - create(name, muscle_group, equipment)
      - update(exercise_id, name, muscle_group, equipment)
      - delete(exercise_id)
    """

    def __init__(self):
        self.repo = ExercisesRepo()

    def list_exercises(self, limit: int = 100):
        return self.repo.list_all(limit=limit)

    def get_exercise(self, exercise_id: int):
        return self.repo.get_by_id(exercise_id)

    def create_exercise(self, name: str, muscle_group: str, equipment: str):
        name = (name or "").strip()
        muscle_group = (muscle_group or "").strip()
        equipment = (equipment or "").strip()

        if len(name) < 2:
            raise ValueError("name must be at least 2 characters")
        if len(muscle_group) < 2:
            raise ValueError("muscle_group is required")
        if len(equipment) < 2:
            raise ValueError("equipment is required")

        return self.repo.create(name, muscle_group, equipment)

    def update_exercise(self, exercise_id: int, name: str, muscle_group: str, equipment: str):
        name = (name or "").strip()
        muscle_group = (muscle_group or "").strip()
        equipment = (equipment or "").strip()

        if len(name) < 2:
            raise ValueError("name must be at least 2 characters")
        if len(muscle_group) < 2:
            raise ValueError("muscle_group is required")
        if len(equipment) < 2:
            raise ValueError("equipment is required")

        return self.repo.update(exercise_id, name, muscle_group, equipment)

    def delete_exercise(self, exercise_id: int):
        return {"deleted": self.repo.delete(exercise_id)}