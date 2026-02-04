from typing import Optional, List, Dict, Any
from app.db import get_conn


class ExercisesRepo:
    def list_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        sql = """
        SELECT exercise_id, name, muscle_group, equipment
        FROM exercises
        ORDER BY exercise_id
        LIMIT %s;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (limit,))
            return cur.fetchall()

    def get_by_id(self, exercise_id: int) -> Optional[Dict[str, Any]]:
        sql = """
        SELECT exercise_id, name, muscle_group, equipment
        FROM exercises
        WHERE exercise_id = %s;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (exercise_id,))
            return cur.fetchone()

    def create(self, name: str, muscle_group: str, equipment: str) -> Dict[str, Any]:
        sql = """
        INSERT INTO exercises (name, muscle_group, equipment)
        VALUES (%s, %s, %s)
        RETURNING exercise_id, name, muscle_group, equipment;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (name, muscle_group, equipment))
            row = cur.fetchone()
            conn.commit()
            return row

    def update(self, exercise_id: int, name: str, muscle_group: str, equipment: str) -> Optional[Dict[str, Any]]:
        sql = """
        UPDATE exercises
        SET name = %s,
            muscle_group = %s,
            equipment = %s
        WHERE exercise_id = %s
        RETURNING exercise_id, name, muscle_group, equipment;
        """
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (name, muscle_group, equipment, exercise_id))
            row = cur.fetchone()
            conn.commit()
            return row

    def delete(self, exercise_id: int) -> bool:
        sql = "DELETE FROM exercises WHERE exercise_id = %s RETURNING exercise_id;"
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(sql, (exercise_id,))
            row = cur.fetchone()
            conn.commit()
            return row is not None
