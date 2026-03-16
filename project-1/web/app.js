const apiBase = window.location.origin;
document.getElementById("apiBasePill").textContent = `API Base: ${apiBase}`;

async function getJson(path) {
  const res = await fetch(path);
  const text = await res.text();

  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = text;
  }

  if (!res.ok) {
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
      const value = row[header] ?? "";
      html += `<td>${value}</td>`;
    });
    html += `</tr>`;
  });

  html += `</tbody></table>`;
  container.innerHTML = html;
}

function getIntValue(id) {
  const raw = document.getElementById(id).value.trim();
  if (!raw) return null;
  const n = parseInt(raw, 10);
  return Number.isFinite(n) ? n : null;
}

async function handleRequest(containerId, path, emptyMessage) {
  const container = document.getElementById(containerId);
  renderMessage(container, "Loading...", "info");

  try {
    const data = await getJson(path);
    renderTable(data, container);
  } catch (err) {
    renderMessage(container, `Error: ${err.message || emptyMessage}`, "error");
  }
}

// Health check
document.getElementById("btnHealth").addEventListener("click", async () => {
  const out = document.getElementById("healthResult");
  out.textContent = "Checking server...";

  try {
    const data = await getJson("/health");
    out.textContent = `Server Status: ${data.status}`;
  } catch (err) {
    out.textContent = `Server Error`;
  }
});

// Users
document.getElementById("btnUsersAll").addEventListener("click", async () => {
  await handleRequest("usersOut", "/users?limit=50", "Could not load users.");
});

document.getElementById("btnUserById").addEventListener("click", async () => {
  const id = getIntValue("userIdInput");
  const container = document.getElementById("usersOut");

  if (!id) {
    renderMessage(container, "Please enter a valid user ID.", "error");
    return;
  }

  await handleRequest("usersOut", `/users/${id}`, "Could not load user.");
});

// Exercises
document.getElementById("btnExercisesAll").addEventListener("click", async () => {
  await handleRequest("exercisesOut", "/exercises?limit=100", "Could not load exercises.");
});

document.getElementById("btnExerciseById").addEventListener("click", async () => {
  const id = getIntValue("exerciseIdInput");
  const container = document.getElementById("exercisesOut");

  if (!id) {
    renderMessage(container, "Please enter a valid exercise ID.", "error");
    return;
  }

  await handleRequest("exercisesOut", `/exercises/${id}`, "Could not load exercise.");
});

// Workouts
document.getElementById("btnWorkoutsAll").addEventListener("click", async () => {
  await handleRequest("workoutsOut", "/workouts?limit=100", "Could not load workouts.");
});

document.getElementById("btnWorkoutById").addEventListener("click", async () => {
  const id = getIntValue("workoutIdInput");
  const container = document.getElementById("workoutsOut");

  if (!id) {
    renderMessage(container, "Please enter a valid workout ID.", "error");
    return;
  }

  await handleRequest("workoutsOut", `/workouts/${id}`, "Could not load workout.");
});

document.getElementById("btnWorkoutsByUser").addEventListener("click", async () => {
  const id = getIntValue("workoutsByUserIdInput");
  const container = document.getElementById("workoutsOut");

  if (!id) {
    renderMessage(container, "Please enter a valid user ID for the workout subset search.", "error");
    return;
  }

  await handleRequest("workoutsOut", `/users/${id}/workouts?limit=50`, "Could not load workouts for that user.");
});