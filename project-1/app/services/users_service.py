from app.repositories.users_repo import UsersRepo


class UsersService:
    """
    Business layer for Users.
    Exposes all CRUD methods in UsersRepo:
      - create(first_name, last_name, email)
      - get_by_id(user_id)
      - list_all(limit)
      - update_email(user_id, new_email)
      - delete(user_id)
    """

    def __init__(self):
        self.repo = UsersRepo()

    def create_user(self, first_name: str, last_name: str, email: str):
        first_name = (first_name or "").strip()
        last_name = (last_name or "").strip()
        email = (email or "").strip()

        if len(first_name) < 1:
            raise ValueError("first_name is required")
        if len(last_name) < 1:
            raise ValueError("last_name is required")
        if "@" not in email or "." not in email:
            raise ValueError("invalid email")

        return self.repo.create(first_name, last_name, email)

    def get_user(self, user_id: int):
        return self.repo.get_by_id(user_id)

    def list_users(self, limit: int = 50):
        return self.repo.list_all(limit=limit)

    def update_user_email(self, user_id: int, new_email: str):
        new_email = (new_email or "").strip()
        if "@" not in new_email or "." not in new_email:
            raise ValueError("invalid email")

        return self.repo.update_email(user_id, new_email)

    def delete_user(self, user_id: int):
        return {"deleted": self.repo.delete(user_id)}