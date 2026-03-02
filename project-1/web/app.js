// Because we are serving this web client FROM FastAPI (same origin),
// we can use relative URLs like "/users" and avoid CORS issues.

const apiBase = window.location.origin; // e.g. http://127.0.0.1:8000
document.getElementById("apiBasePill").textContent = `API Base: ${apiBase}`;

async function getJson(path) {
  const res = await fetch(path, { method: "GET" });
  const text = await res.text();

  // Try to parse JSON if possible, otherwise show raw text
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }

  if (!res.ok) {
    throw new Error(`HTTP ${res.status} - ${typeof data === "string" ? data : JSON.stringify(data)}`);
  }
  return data;
}

function pretty(outEl, data) {
  outEl.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

function valInt(id) {
  const raw = document.getElementById(id).value;
  const n = parseInt(raw, 10);
  return Number.isFinite(n) ? n : null;
}

// Health
document.getElementById("btnHealth").addEventListener("click", async () => {
  const out = document.getElementById("healthResult");
  out.textContent = "Checking...";
  try {
    const data = await getJson("/health");
    out.textContent = `OK: ${JSON.stringify(data)}`;
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Users: GET all
document.getElementById("btnUsersAll").addEventListener("click", async () => {
  const out = document.getElementById("usersOut");
  out.textContent = "Loading...";
  try {
    const data = await getJson("/users?limit=50");
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Users: GET by id
document.getElementById("btnUserById").addEventListener("click", async () => {
  const out = document.getElementById("usersOut");
  const id = valInt("userIdInput");
  if (!id) {
    out.textContent = "Enter a valid user_id (e.g., 1).";
    return;
  }
  out.textContent = "Loading...";
  try {
    const data = await getJson(`/users/${id}`);
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Exercises: GET all
document.getElementById("btnExercisesAll").addEventListener("click", async () => {
  const out = document.getElementById("exercisesOut");
  out.textContent = "Loading...";
  try {
    const data = await getJson("/exercises?limit=100");
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Exercises: GET by id
document.getElementById("btnExerciseById").addEventListener("click", async () => {
  const out = document.getElementById("exercisesOut");
  const id = valInt("exerciseIdInput");
  if (!id) {
    out.textContent = "Enter a valid exercise_id (e.g., 1).";
    return;
  }
  out.textContent = "Loading...";
  try {
    const data = await getJson(`/exercises/${id}`);
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Workouts: GET all
document.getElementById("btnWorkoutsAll").addEventListener("click", async () => {
  const out = document.getElementById("workoutsOut");
  out.textContent = "Loading...";
  try {
    const data = await getJson("/workouts?limit=100");
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Workouts: GET by id
document.getElementById("btnWorkoutById").addEventListener("click", async () => {
  const out = document.getElementById("workoutsOut");
  const id = valInt("workoutIdInput");
  if (!id) {
    out.textContent = "Enter a valid workout_id (e.g., 1).";
    return;
  }
  out.textContent = "Loading...";
  try {
    const data = await getJson(`/workouts/${id}`);
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});

// Workouts: GET subset by user
document.getElementById("btnWorkoutsByUser").addEventListener("click", async () => {
  const out = document.getElementById("workoutsOut");
  const userId = valInt("workoutsByUserIdInput");
  if (!userId) {
    out.textContent = "Enter a valid user_id (e.g., 1).";
    return;
  }
  out.textContent = "Loading...";
  try {
    const data = await getJson(`/users/${userId}/workouts?limit=50`);
    pretty(out, data);
  } catch (e) {
    out.textContent = `Error: ${e.message}`;
  }
});