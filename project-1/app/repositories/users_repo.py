from app.db import get_conn

class UsersRepo:
    def create(self, first_name, last_name, email):
        sql = """
        INSERT INTO users (first_name, last_name, email)
        VALUES (%s, %s, %s)
        RETURNING user_id, first_name, last_name, email, created_at;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (first_name, last_name, email))
            return cur.fetchone()

    def get_by_id(self, user_id: int):
        sql = "SELECT user_id, first_name, last_name, email, created_at FROM users WHERE user_id = %s;"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.fetchone()

    def list_all(self, limit=50):
        sql = "SELECT user_id, first_name, last_name, email, created_at FROM users ORDER BY user_id LIMIT %s;"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()

    def update_email(self, user_id: int, new_email: str):
        sql = """
        UPDATE users SET email = %s
        WHERE user_id = %s
        RETURNING user_id, first_name, last_name, email, created_at;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (new_email, user_id))
            return cur.fetchone()

    def delete(self, user_id: int) -> bool:
        sql = "DELETE FROM users WHERE user_id = %s;"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (user_id,))
            return cur.rowcount == 1
