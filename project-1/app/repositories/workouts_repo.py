from typing import Optional, List, Dict, Any
from app.db import get_conn


class WorkoutsRepo:
    def list_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        sql = """
        SELECT workout_id, user_id, workout_date, name, notes
        FROM workouts
        ORDER BY workout_date DESC, workout_id DESC
        LIMIT %s;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()

    def list_by_user(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        sql = """
        SELECT workout_id, user_id, workout_date, name, notes
        FROM workouts
        WHERE user_id = %s
        ORDER BY workout_date DESC, workout_id DESC
        LIMIT %s;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (user_id, limit))
            return cur.fetchall()

    def get_by_id(self, workout_id: int) -> Optional[Dict[str, Any]]:
        sql = """
        SELECT workout_id, user_id, workout_date, name, notes
        FROM workouts
        WHERE workout_id = %s;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (workout_id,))
            return cur.fetchone()

    def create(self, user_id: int, workout_date, name: str, notes: str = "") -> Dict[str, Any]:
        """
        workout_date can be a datetime.date or a 'YYYY-MM-DD' string.
        """
        sql = """
        INSERT INTO workouts (user_id, workout_date, name, notes)
        VALUES (%s, %s, %s, %s)
        RETURNING workout_id, user_id, workout_date, name, notes;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (user_id, workout_date, name, notes))
            row = cur.fetchone()
            conn.commit()
            return row

    def update(self, workout_id: int, workout_date, name: str, notes: str = "") -> Optional[Dict[str, Any]]:
        sql = """
        UPDATE workouts
        SET workout_date = %s,
            name = %s,
            notes = %s
        WHERE workout_id = %s
        RETURNING workout_id, user_id, workout_date, name, notes;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (workout_date, name, notes, workout_id))
            row = cur.fetchone()
            conn.commit()
            return row

    def delete(self, workout_id: int) -> bool:
        sql = "DELETE FROM workouts WHERE workout_id = %s RETURNING workout_id;"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (workout_id,))
            row = cur.fetchone()
            conn.commit()
            return row is not None
