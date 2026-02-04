from app.repositories.users_repo import UsersRepo
from app.db import get_conn

users_repo = UsersRepo()

def list_workouts_for_user(user_id: int):
    sql = """
    SELECT w.workout_id, w.workout_date, w.name
    FROM workouts w
    WHERE w.user_id = %s
    ORDER BY w.workout_date DESC, w.workout_id DESC
    LIMIT 20;
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchall()

def menu():
    print("\n=== Workout Tracker Console ===")
    print("1) List users")
    print("2) Get user by id")
    print("3) Create user")
    print("4) Update user email")
    print("5) Delete user")
    print("6) List workouts for a user")
    print("0) Exit")

def main():
    while True:
        menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            rows = users_repo.list_all()
            for r in rows:
                print(r)

        elif choice == "2":
            uid = int(input("User ID: "))
            print(users_repo.get_by_id(uid))

        elif choice == "3":
            fn = input("First name: ").strip()
            ln = input("Last name: ").strip()
            em = input("Email: ").strip()
            print(users_repo.create(fn, ln, em))

        elif choice == "4":
            uid = int(input("User ID: "))
            em = input("New email: ").strip()
            print(users_repo.update_email(uid, em))

        elif choice == "5":
            uid = int(input("User ID: "))
            ok = users_repo.delete(uid)
            print("Deleted." if ok else "Not found.")

        elif choice == "6":
            uid = int(input("User ID: "))
            workouts = list_workouts_for_user(uid)
            for w in workouts:
                print(w)

        elif choice == "0":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
