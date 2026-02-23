import time
import requests

BASE = "http://127.0.0.1:8000"

def safe_json(r: requests.Response):
    try:
        return r.json()
    except Exception:
        return None

def call(method, path, params=None):
    url = f"{BASE}{path}"
    r = requests.request(method, url, params=params)
    print(f"\n{method} {r.url}")
    print("STATUS:", r.status_code)
    print("CONTENT-TYPE:", r.headers.get("Content-Type", ""))

    data = safe_json(r)
    if data is not None:
        print("JSON:", data)
    else:
        print("BODY:", r.text[:1000])

    if r.status_code >= 400:
        raise SystemExit("Stopped due to error status code.")
    return data

def main():
    call("GET", "/health")

    unique_email = f"p2test_{time.time_ns()}@example.com"

    # USERS CRUD
    user = call("POST", "/users", params={
        "first_name": "Project2",
        "last_name": "Test",
        "email": unique_email
    })
    user_id = user["user_id"]

    call("GET", f"/users/{user_id}")
    call("PUT", f"/users/{user_id}/email", params={"new_email": f"updated_{time.time_ns()}@example.com"})
    call("GET", f"/users/{user_id}")
    call("DELETE", f"/users/{user_id}")

    # EXERCISES CRUD
    ex = call("POST", "/exercises", params={
        "name": "P2 Test Exercise",
        "muscle_group": "Biceps",
        "equipment": "Dumbbell"
    })
    ex_id = ex["exercise_id"]

    call("GET", f"/exercises/{ex_id}")
    call("PUT", f"/exercises/{ex_id}", params={
        "name": "P2 Test Exercise Updated",
        "muscle_group": "Biceps",
        "equipment": "Dumbbell"
    })
    call("DELETE", f"/exercises/{ex_id}")

    # WORKOUTS CRUD (assumes user_id=1 exists)
    w = call("POST", "/workouts", params={
        "user_id": 1,
        "workout_date": "2026-02-23",
        "name": "P2 Demo Workout",
        "notes": "From console client"
    })
    w_id = w["workout_id"]

    call("GET", f"/workouts/{w_id}")
    call("PUT", f"/workouts/{w_id}", params={
        "workout_date": "2026-02-24",
        "name": "P2 Demo Workout Updated",
        "notes": "Updated notes"
    })
    call("DELETE", f"/workouts/{w_id}")

    print("\n✅ Console client CRUD proof complete.")

if __name__ == "__main__":
    main()