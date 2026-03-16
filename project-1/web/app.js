const apiBase = window.location.origin;
document.getElementById("apiBasePill").textContent = `API Base: ${apiBase}`;

async function requestJson(method, path, params = null) {
  let url = path;

  if (params) {
    const query = new URLSearchParams(params);
    url += `?${query.toString()}`;
  }

  const response = await fetch(url, { method });
  const text = await response.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }

  if (!response.ok) {
    throw new Error(typeof data === "string" ? data : JSON.stringify(data));
  }

  return data;
}

function renderMessage(container, message, type = "info") {
  container.innerHTML = `<p class="message ${type}">${message}</p>`;
}

function formatHeader(key) {
  return key.replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function renderTable(data, container) {
  if (!data) {
    renderMessage(container, "No data found.", "info");
    return;
  }

  const rows = Array.isArray(data) ? data : [data];

  if (rows.length === 0) {
    renderMessage(container, "No matching records were found.", "info");
    return;
  }

  const headers = Object.keys(rows[0]);

  let html = `<table class="data-table"><thead><tr>`;
  headers.forEach((header) => {
    html += `<th>${formatHeader(header)}</th>`;
  });
  html += `</tr></thead><tbody>`;

  rows.forEach((row) => {
    html += `<tr>`;
    headers.forEach((header) => {
      html += `<td>${row[header] ?? ""}</td>`;
    });
    html += `</tr>`;
  });

  html += `</tbody></table>`;
  container.innerHTML = html;
}

function getValue(id) {
  return document.getElementById(id).value.trim();
}

function getIntValue(id) {
  const value = getValue(id);
  if (!value) return null;
  const n = parseInt(value, 10);
  return Number.isFinite(n) ? n : null;
}

async function handleGet(containerId, path, emptyMessage) {
  const container = document.getElementById(containerId);
  renderMessage(container, "Loading...", "info");

  try {
    const data = await requestJson("GET", path);
    renderTable(data, container);
  } catch (err) {
    renderMessage(container, `Error: ${err.message || emptyMessage}`, "error");
  }
}

async function handleWrite(containerId, method, path, params, successMessage) {
  const container = document.getElementById(containerId);
  renderMessage(container, "Processing request...", "info");

  try {
    const data = await requestJson(method, path, params);
    renderMessage(container, successMessage, "success");
    renderTable(data, container);
  } catch (err) {
    renderMessage(container, `Error: ${err.message}`, "error");
  }
}

// -------------------
// HEALTH
// -------------------
document.getElementById("btnHealth").addEventListener("click", async () => {
  const out = document.getElementById("healthResult");
  out.textContent = "Checking server...";

  try {
    const data = await requestJson("GET", "/health");
    out.textContent = `Server Status: ${data.status}`;
  } catch {
    out.textContent = "Server Error";
  }
});

// -------------------
// USERS
// -------------------
document.getElementById("btnUsersAll").addEventListener("click", async () => {
  await handleGet("usersOut", "/users?limit=50", "Could not load users.");
});

document.getElementById("btnUserById").addEventListener("click", async () => {
  const id = getIntValue("userIdInput");
  const container = document.getElementById("usersOut");

  if (!id) {
    renderMessage(container, "Please enter a valid user ID.", "error");
    return;
  }

  await handleGet("usersOut", `/users/${id}`, "Could not load user.");
});

document.getElementById("btnCreateUser").addEventListener("click", async () => {
  const first_name = getValue("userFirstName");
  const last_name = getValue("userLastName");
  const email = getValue("userEmail");
  const container = document.getElementById("usersOut");

  if (!first_name || !last_name || !email) {
    renderMessage(container, "Please enter first name, last name, and email.", "error");
    return;
  }

  await handleWrite(
    "usersOut",
    "POST",
    "/users",
    { first_name, last_name, email },
    "User created successfully."
  );
});

document.getElementById("btnUpdateUser").addEventListener("click", async () => {
  const user_id = getIntValue("userUpdateId");
  const new_email = getValue("userUpdateEmail");
  const container = document.getElementById("usersOut");

  if (!user_id || !new_email) {
    renderMessage(container, "Please enter a valid user ID and a new email.", "error");
    return;
  }

  await handleWrite(
    "usersOut",
    "PUT",
    `/users/${user_id}/email`,
    { new_email },
    "User email updated successfully."
  );
});

// -------------------
// EXERCISES
// -------------------
document.getElementById("btnExercisesAll").addEventListener("click", async () => {
  await handleGet("exercisesOut", "/exercises?limit=100", "Could not load exercises.");
});

document.getElementById("btnExerciseById").addEventListener("click", async () => {
  const id = getIntValue("exerciseIdInput");
  const container = document.getElementById("exercisesOut");

  if (!id) {
    renderMessage(container, "Please enter a valid exercise ID.", "error");
    return;
  }

  await handleGet("exercisesOut", `/exercises/${id}`, "Could not load exercise.");
});

document.getElementById("btnCreateExercise").addEventListener("click", async () => {
  const name = getValue("exerciseName");
  const muscle_group = getValue("exerciseMuscleGroup");
  const equipment = getValue("exerciseEquipment");
  const container = document.getElementById("exercisesOut");

  if (!name || !muscle_group || !equipment) {
    renderMessage(container, "Please enter name, muscle group, and equipment.", "error");
    return;
  }

  await handleWrite(
    "exercisesOut",
    "POST",
    "/exercises",
    { name, muscle_group, equipment },
    "Exercise created successfully."
  );
});

document.getElementById("btnUpdateExercise").addEventListener("click", async () => {
  const exercise_id = getIntValue("exerciseUpdateId");
  const name = getValue("exerciseUpdateName");
  const muscle_group = getValue("exerciseUpdateMuscleGroup");
  const equipment = getValue("exerciseUpdateEquipment");
  const container = document.getElementById("exercisesOut");

  if (!exercise_id || !name || !muscle_group || !equipment) {
    renderMessage(container, "Please enter exercise ID, name, muscle group, and equipment.", "error");
    return;
  }

  await handleWrite(
    "exercisesOut",
    "PUT",
    `/exercises/${exercise_id}`,
    { name, muscle_group, equipment },
    "Exercise updated successfully."
  );
});

// -------------------
// WORKOUTS
// -------------------
document.getElementById("btnWorkoutsAll").addEventListener("click", async () => {
  await handleGet("workoutsOut", "/workouts?limit=100", "Could not load workouts.");
});

document.getElementById("btnWorkoutById").addEventListener("click", async () => {
  const id = getIntValue("workoutIdInput");
  const container = document.getElementById("workoutsOut");

  if (!id) {
    renderMessage(container, "Please enter a valid workout ID.", "error");
    return;
  }

  await handleGet("workoutsOut", `/workouts/${id}`, "Could not load workout.");
});

document.getElementById("btnWorkoutsByUser").addEventListener("click", async () => {
  const id = getIntValue("workoutsByUserIdInput");
  const container = document.getElementById("workoutsOut");

  if (!id) {
    renderMessage(container, "Please enter a valid user ID for the workout search.", "error");
    return;
  }

  await handleGet("workoutsOut", `/users/${id}/workouts?limit=50`, "Could not load workouts for that user.");
});

document.getElementById("btnCreateWorkout").addEventListener("click", async () => {
  const user_id = getIntValue("workoutCreateUserId");
  const workout_date = getValue("workoutCreateDate");
  const name = getValue("workoutCreateName");
  const notes = getValue("workoutCreateNotes");
  const container = document.getElementById("workoutsOut");

  if (!user_id || !workout_date || !name) {
    renderMessage(container, "Please enter user ID, workout date, and workout name.", "error");
    return;
  }

  await handleWrite(
    "workoutsOut",
    "POST",
    "/workouts",
    { user_id, workout_date, name, notes },
    "Workout created successfully."
  );
});

document.getElementById("btnUpdateWorkout").addEventListener("click", async () => {
  const workout_id = getIntValue("workoutUpdateId");
  const workout_date = getValue("workoutUpdateDate");
  const name = getValue("workoutUpdateName");
  const notes = getValue("workoutUpdateNotes");
  const container = document.getElementById("workoutsOut");

  if (!workout_id || !workout_date || !name) {
    renderMessage(container, "Please enter workout ID, workout date, and workout name.", "error");
    return;
  }

  await handleWrite(
    "workoutsOut",
    "PUT",
    `/workouts/${workout_id}`,
    { workout_date, name, notes },
    "Workout updated successfully."
  );
});