from datetime import datetime
from app.repositories.users_repo import UsersRepo
from app.db import get_conn

users_repo = UsersRepo()


def print_header(title: str) -> None:
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def print_kv(label: str, value) -> None:
    print(f"{label:<14}: {value}")


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


def format_dt(dt_val):
    """Handles datetime values coming from psycopg2."""
    if isinstance(dt_val, datetime):
        return dt_val.strftime("%Y-%m-%d %H:%M:%S")
    return dt_val


def action_list_users():
    print_header("USERS (first 50)")
    rows = users_repo.list_all()
    if not rows:
        print("No users found.")
        return

    for r in rows:
        created = format_dt(r.get("created_at"))
        print(f"ID {r['user_id']:>2}  |  {r['first_name']} {r['last_name']:<10} |  {r['email']:<22} |  {created}")


def action_get_user_by_id():
    uid = int(input("User ID: ").strip())
    r = users_repo.get_by_id(uid)

    print_header(f"USER DETAILS (id={uid})")
    if not r:
        print("User not found.")
        return

    print_kv("User ID", r["user_id"])
    print_kv("First name", r["first_name"])
    print_kv("Last name", r["last_name"])
    print_kv("Email", r["email"])
    print_kv("Created", format_dt(r.get("created_at")))


def action_create_user():
    print_header("CREATE USER")
    fn = input("First name: ").strip()
    ln = input("Last name: ").strip()
    em = input("Email: ").strip()

    try:
        r = users_repo.create(fn, ln, em)
        print("\n✅ User created:")
        print_kv("User ID", r["user_id"])
        print_kv("Name", f"{r['first_name']} {r['last_name']}")
        print_kv("Email", r["email"])
        print_kv("Created", format_dt(r.get("created_at")))
    except Exception as e:
        print(f"\n❌ Could not create user: {e}")


def action_update_user_email():
    print_header("UPDATE USER EMAIL")
    uid = int(input("User ID: ").strip())
    em = input("New email: ").strip()

    try:
        r = users_repo.update_email(uid, em)
        if not r:
            print("User not found.")
            return
        print("\n✅ Email updated:")
        print_kv("User ID", r["user_id"])
        print_kv("Name", f"{r['first_name']} {r['last_name']}")
        print_kv("Email", r["email"])
    except Exception as e:
        print(f"\n❌ Could not update email: {e}")


def action_delete_user():
    print_header("DELETE USER")
    uid = int(input("User ID: ").strip())

    try:
        ok = users_repo.delete(uid)
        print("\n✅ Deleted." if ok else "\nUser not found.")
    except Exception as e:
        print(f"\n❌ Could not delete user: {e}")


def action_list_workouts_for_user():
    print_header("WORKOUTS FOR USER")
    uid = int(input("User ID: ").strip())

    rows = list_workouts_for_user(uid)
    if not rows:
        print("No workouts found for that user.")
        return

    # Table-like output
    print(f"{'Workout ID':<10}  {'Date':<12}  {'Name'}")
    print("-" * 40)
    for w in rows:
        print(f"{w['workout_id']:<10}  {str(w['workout_date']):<12}  {w['name']}")


def main():
    while True:
        menu()
        choice = input("Choose: ").strip()

        if choice == "1":
            action_list_users()

        elif choice == "2":
            action_get_user_by_id()

        elif choice == "3":
            action_create_user()

        elif choice == "4":
            action_update_user_email()

        elif choice == "5":
            action_delete_user()

        elif choice == "6":
            action_list_workouts_for_user()

        elif choice == "0":
            print("\nGoodbye!")
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
