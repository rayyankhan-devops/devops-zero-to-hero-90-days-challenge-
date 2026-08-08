/* ============================================================
   SecureVault — Frontend Application Logic
   ============================================================ */

"use strict";

// ── Configuration ──────────────────────────────────────────
const API_BASE = "/api";

// ── State ──────────────────────────────────────────────────
let authToken = localStorage.getItem("sv_token") || null;
let currentUser = JSON.parse(localStorage.getItem("sv_user") || "null");
let allNotes = [];
let allTasks = [];
let currentNoteColor = "default";
let currentPage = "dashboard";

// ── Utility: HTTP Client ───────────────────────────────────
async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  if (authToken) headers["Authorization"] = `Bearer ${authToken}`;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { ...headers, ...(options.headers || {}) },
  });

  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
}

// ── Toast Notifications ────────────────────────────────────
function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  const icons = {
    success: "check-circle",
    error: "alert-circle",
    info: "info",
  };

  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-icon"><i data-lucide="${icons[type]}"></i></div>
    <span class="toast-message">${escapeHtml(message)}</span>
  `;
  container.appendChild(toast);
  lucide.createIcons({ nodes: [toast] });

  setTimeout(() => {
    toast.style.animation = "none";
    toast.style.opacity = "0";
    toast.style.transform = "translateX(30px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ── HTML Escaping (XSS prevention) ────────────────────────
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ── Date Formatting ────────────────────────────────────────
function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function formatDateTime(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function isOverdue(iso) {
  return iso && new Date(iso) < new Date();
}

// ── Password Toggle ────────────────────────────────────────
function togglePassword(inputId) {
  const input = document.getElementById(inputId);
  const eyeId = inputId === "login-password" ? "login-eye" : "reg-eye";
  if (input.type === "password") {
    input.type = "text";
    document.getElementById(eyeId).setAttribute("data-lucide", "eye-off");
  } else {
    input.type = "password";
    document.getElementById(eyeId).setAttribute("data-lucide", "eye");
  }
  lucide.createIcons();
}

// ── Auth Tab Switching ─────────────────────────────────────
function switchTab(tab) {
  const loginForm = document.getElementById("login-form");
  const registerForm = document.getElementById("register-form");
  const tabLogin = document.getElementById("tab-login");
  const tabRegister = document.getElementById("tab-register");

  if (tab === "login") {
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");
    tabLogin.classList.add("active");
    tabRegister.classList.remove("active");
    clearAuthErrors();
  } else {
    loginForm.classList.add("hidden");
    registerForm.classList.remove("hidden");
    tabLogin.classList.remove("active");
    tabRegister.classList.add("active");
    clearAuthErrors();
  }
}

function clearAuthErrors() {
  document.getElementById("login-error").classList.add("hidden");
  document.getElementById("reg-error").classList.add("hidden");
}

function setButtonLoading(btnId, loading) {
  const btn = document.getElementById(btnId);
  const text = btn.querySelector(".btn-text");
  const spinner = btn.querySelector(".btn-spinner");
  btn.disabled = loading;
  text.classList.toggle("hidden", loading);
  spinner.classList.toggle("hidden", !loading);
}

// ── AUTH: Login ────────────────────────────────────────────
async function handleLogin(e) {
  e.preventDefault();
  const identifier = document.getElementById("login-identifier").value.trim();
  const password = document.getElementById("login-password").value;
  const errorEl = document.getElementById("login-error");

  errorEl.classList.add("hidden");
  setButtonLoading("login-btn", true);

  const { ok, data } = await api("/auth/login", {
    method: "POST",
    body: JSON.stringify({ identifier, password }),
  });

  setButtonLoading("login-btn", false);

  if (ok) {
    saveAuthSession(data.token, data.user);
    showApp();
  } else {
    errorEl.textContent = data.error || "Login failed. Please try again.";
    errorEl.classList.remove("hidden");
  }
}

// ── AUTH: Register ─────────────────────────────────────────
async function handleRegister(e) {
  e.preventDefault();
  const username = document.getElementById("reg-username").value.trim();
  const email = document.getElementById("reg-email").value.trim();
  const password = document.getElementById("reg-password").value;
  const errorEl = document.getElementById("reg-error");

  errorEl.classList.add("hidden");
  setButtonLoading("register-btn", true);

  const { ok, data } = await api("/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, email, password }),
  });

  setButtonLoading("register-btn", false);

  if (ok) {
    saveAuthSession(data.token, data.user);
    showApp();
    showToast("Welcome to SecureVault! 🎉", "success");
  } else {
    errorEl.textContent = data.error || "Registration failed. Please try again.";
    errorEl.classList.remove("hidden");
  }
}

function saveAuthSession(token, user) {
  authToken = token;
  currentUser = user;
  localStorage.setItem("sv_token", token);
  localStorage.setItem("sv_user", JSON.stringify(user));
}

function logout() {
  authToken = null;
  currentUser = null;
  localStorage.removeItem("sv_token");
  localStorage.removeItem("sv_user");
  allNotes = [];
  allTasks = [];
  showAuth();
  showToast("You've been logged out", "info");
}

// ── Screen Management ──────────────────────────────────────
function showAuth() {
  document.getElementById("auth-screen").classList.remove("hidden");
  document.getElementById("app-screen").classList.add("hidden");
}

function showApp() {
  document.getElementById("auth-screen").classList.add("hidden");
  document.getElementById("app-screen").classList.remove("hidden");
  updateSidebarUser();
  navigate("dashboard");
}

function updateSidebarUser() {
  if (!currentUser) return;
  document.getElementById("sidebar-username").textContent = currentUser.username;
  document.getElementById("sidebar-email").textContent = currentUser.email;
  document.getElementById("sidebar-avatar").textContent = currentUser.username.charAt(0).toUpperCase();
}

// ── Navigation ─────────────────────────────────────────────
function navigate(page) {
  currentPage = page;

  // Hide all pages
  document.querySelectorAll(".page").forEach((p) => {
    p.classList.add("hidden");
    p.classList.remove("active");
  });

  // Show target page
  const target = document.getElementById(`page-${page}`);
  if (target) {
    target.classList.remove("hidden");
    target.classList.add("active");
  }

  // Update nav items
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.remove("active");
  });
  const navItem = document.getElementById(`nav-${page}`);
  if (navItem) navItem.classList.add("active");

  // Update topbar title
  const titles = { dashboard: "Dashboard", notes: "Notes", tasks: "Tasks" };
  document.getElementById("topbar-title").textContent = titles[page] || page;

  // Load page data
  if (page === "dashboard") loadDashboard();
  if (page === "notes") loadNotes();
  if (page === "tasks") loadTasks();

  // Close sidebar on mobile
  if (window.innerWidth <= 768) {
    document.getElementById("sidebar").classList.remove("open");
  }
}

// ── Sidebar Toggle ─────────────────────────────────────────
function toggleSidebar() {
  document.getElementById("sidebar").classList.toggle("open");
}

// ── DASHBOARD ─────────────────────────────────────────────
async function loadDashboard() {
  updateGreeting();
  await Promise.all([loadDashboardStats(), loadRecentNotes(), loadPriorityTasks()]);
}

function updateGreeting() {
  const hour = new Date().getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const name = currentUser ? currentUser.username : "there";
  document.getElementById("dashboard-greeting").textContent = `${greeting}, ${name}! 👋`;
}

async function loadDashboardStats() {
  const { ok, data } = await api("/tasks/stats");
  if (ok) {
    document.getElementById("stat-total").textContent = data.total;
    document.getElementById("stat-todo").textContent = data.todo;
    document.getElementById("stat-inprogress").textContent = data.in_progress;
    document.getElementById("stat-done").textContent = data.done;
  }
}

async function loadRecentNotes() {
  const { ok, data } = await api("/notes/");
  if (!ok) return;

  const container = document.getElementById("recent-notes-list");
  const notes = data.notes.slice(0, 4);

  if (notes.length === 0) {
    container.innerHTML = `
      <div class="empty-state-sm">
        <i data-lucide="sticky-note"></i>
        <p>No notes yet</p>
      </div>`;
    lucide.createIcons({ nodes: [container] });
    return;
  }

  container.innerHTML = notes
    .map(
      (note) => `
    <div class="recent-item" onclick="navigate('notes')">
      <div class="recent-item-icon"><i data-lucide="file-text"></i></div>
      <div class="recent-item-info">
        <div class="recent-item-title">${escapeHtml(note.title)}</div>
        <div class="recent-item-meta">${formatDate(note.updated_at)}</div>
      </div>
    </div>`
    )
    .join("");
  lucide.createIcons({ nodes: [container] });
}

async function loadPriorityTasks() {
  const { ok, data } = await api("/tasks/");
  if (!ok) return;

  const container = document.getElementById("priority-tasks-list");
  const high = data.tasks.filter((t) => t.priority === "high" && t.status !== "done").slice(0, 4);

  if (high.length === 0) {
    container.innerHTML = `
      <div class="empty-state-sm">
        <i data-lucide="alert-circle"></i>
        <p>No high priority tasks</p>
      </div>`;
    lucide.createIcons({ nodes: [container] });
    return;
  }

  container.innerHTML = high
    .map(
      (t) => `
    <div class="recent-item" onclick="navigate('tasks')">
      <div class="recent-item-icon" style="background: rgba(244,63,94,0.15); color: #fb7185;"><i data-lucide="alert-circle"></i></div>
      <div class="recent-item-info">
        <div class="recent-item-title">${escapeHtml(t.title)}</div>
        <div class="recent-item-meta">${statusLabel(t.status)}</div>
      </div>
    </div>`
    )
    .join("");
  lucide.createIcons({ nodes: [container] });
}

// ── NOTES ──────────────────────────────────────────────────
async function loadNotes() {
  const { ok, data } = await api("/notes/");
  if (!ok) {
    showToast("Failed to load notes", "error");
    return;
  }
  allNotes = data.notes;
  renderNotes(allNotes);
}

function renderNotes(notes) {
  const grid = document.getElementById("notes-grid");
  const emptyEl = document.getElementById("notes-empty");

  // Clear existing note cards only
  grid.querySelectorAll(".note-card").forEach((c) => c.remove());

  if (notes.length === 0) {
    emptyEl.classList.remove("hidden");
    return;
  }
  emptyEl.classList.add("hidden");

  notes.forEach((note) => {
    const card = createNoteCard(note);
    grid.appendChild(card);
  });
  lucide.createIcons({ nodes: [grid] });
}

function createNoteCard(note) {
  const card = document.createElement("div");
  card.className = "note-card";
  card.dataset.color = note.color || "default";
  card.dataset.id = note.id;

  card.innerHTML = `
    <div class="note-card-accent"></div>
    <div class="note-card-header">
      <div class="note-card-title">${escapeHtml(note.title)}</div>
      <div class="note-card-actions">
        <button class="btn-icon" onclick="event.stopPropagation(); openNoteModal(${note.id})" title="Edit">
          <i data-lucide="pencil"></i>
        </button>
        <button class="btn-icon" onclick="event.stopPropagation(); confirmDelete('note', ${note.id})" title="Delete">
          <i data-lucide="trash-2"></i>
        </button>
      </div>
    </div>
    <div class="note-card-body">${escapeHtml(note.content)}</div>
    <div class="note-card-footer">
      <span class="note-card-date">${formatDate(note.updated_at)}</span>
      ${note.is_pinned ? `<span class="pin-badge"><i data-lucide="pin"></i> Pinned</span>` : ""}
    </div>
  `;

  card.addEventListener("click", () => openNoteModal(note.id));
  return card;
}

function filterNotes(query) {
  const lower = query.toLowerCase();
  const filtered = allNotes.filter(
    (n) =>
      n.title.toLowerCase().includes(lower) || n.content.toLowerCase().includes(lower)
  );
  renderNotes(filtered);
}

// Note Modal
function openNoteModal(noteId = null) {
  const modal = document.getElementById("note-modal");
  const titleEl = document.getElementById("note-modal-title");
  const form = document.getElementById("note-form");

  form.reset();
  currentNoteColor = "default";
  resetColorPicker();

  if (noteId) {
    const note = allNotes.find((n) => n.id === noteId);
    if (!note) return;
    titleEl.textContent = "Edit Note";
    document.getElementById("note-id").value = note.id;
    document.getElementById("note-title").value = note.title;
    document.getElementById("note-content").value = note.content;
    document.getElementById("note-pinned").checked = note.is_pinned;
    selectColorByValue(note.color || "default");
  } else {
    titleEl.textContent = "New Note";
    document.getElementById("note-id").value = "";
  }

  modal.classList.remove("hidden");
}

function closeNoteModal(event) {
  if (event && event.target !== document.getElementById("note-modal")) return;
  document.getElementById("note-modal").classList.add("hidden");
}

function selectColor(color, btn) {
  currentNoteColor = color;
  document.querySelectorAll(".color-dot").forEach((d) => d.classList.remove("active"));
  btn.classList.add("active");
}

function resetColorPicker() {
  const dots = document.querySelectorAll(".color-dot");
  dots.forEach((d) => d.classList.remove("active"));
  if (dots[0]) dots[0].classList.add("active");
  currentNoteColor = "default";
}

function selectColorByValue(color) {
  const dot = document.querySelector(`.color-dot[data-color="${color}"]`);
  if (dot) {
    document.querySelectorAll(".color-dot").forEach((d) => d.classList.remove("active"));
    dot.classList.add("active");
    currentNoteColor = color;
  }
}

async function saveNote(e) {
  e.preventDefault();
  const noteId = document.getElementById("note-id").value;
  const payload = {
    title: document.getElementById("note-title").value.trim(),
    content: document.getElementById("note-content").value.trim(),
    is_pinned: document.getElementById("note-pinned").checked,
    color: currentNoteColor,
  };

  const isEdit = !!noteId;
  const { ok, data } = isEdit
    ? await api(`/notes/${noteId}`, { method: "PUT", body: JSON.stringify(payload) })
    : await api("/notes/", { method: "POST", body: JSON.stringify(payload) });

  if (ok) {
    showToast(isEdit ? "Note updated!" : "Note created!", "success");
    document.getElementById("note-modal").classList.add("hidden");
    await loadNotes();
    if (currentPage === "dashboard") loadDashboardStats();
  } else {
    showToast(data.error || "Failed to save note", "error");
  }
}

// ── TASKS ──────────────────────────────────────────────────
async function loadTasks(statusFilter = "all") {
  const url = statusFilter !== "all" ? `/tasks/?status=${statusFilter}` : "/tasks/";
  const { ok, data } = await api(url);
  if (!ok) {
    showToast("Failed to load tasks", "error");
    return;
  }
  allTasks = data.tasks;
  renderTasks(allTasks);
}

function renderTasks(tasks) {
  const list = document.getElementById("tasks-list");
  const emptyEl = document.getElementById("tasks-empty");

  list.querySelectorAll(".task-card").forEach((c) => c.remove());

  if (tasks.length === 0) {
    emptyEl.classList.remove("hidden");
    return;
  }
  emptyEl.classList.add("hidden");

  tasks.forEach((task) => {
    const card = createTaskCard(task);
    list.appendChild(card);
  });
  lucide.createIcons({ nodes: [list] });
}

function statusLabel(status) {
  const labels = { todo: "To Do", in_progress: "In Progress", done: "Done" };
  return labels[status] || status;
}

function priorityLabel(priority) {
  return priority.charAt(0).toUpperCase() + priority.slice(1);
}

function createTaskCard(task) {
  const overdue = isOverdue(task.due_date) && task.status !== "done";
  const card = document.createElement("div");
  card.className = `task-card status-${task.status}`;
  card.dataset.status = task.status;
  card.dataset.id = task.id;

  card.innerHTML = `
    <div class="task-status-dot"></div>
    <div class="task-body">
      <div class="task-title">${escapeHtml(task.title)}</div>
      ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ""}
      <div class="task-meta">
        <span class="badge badge-status-${task.status}">${statusLabel(task.status)}</span>
        <span class="badge badge-priority-${task.priority}">${priorityLabel(task.priority)}</span>
        ${
          task.due_date
            ? `<span class="task-due ${overdue ? "overdue" : ""}">
                <i data-lucide="calendar"></i>
                ${formatDateTime(task.due_date)}${overdue ? " · Overdue" : ""}
              </span>`
            : ""
        }
      </div>
    </div>
    <div class="task-actions">
      <button class="btn-icon" onclick="openTaskModal(${task.id})" title="Edit">
        <i data-lucide="pencil"></i>
      </button>
      <button class="btn-icon" onclick="confirmDelete('task', ${task.id})" title="Delete">
        <i data-lucide="trash-2"></i>
      </button>
    </div>
  `;

  return card;
}

function filterTasks(status) {
  document.querySelectorAll(".filter-tab").forEach((t) => {
    t.classList.toggle("active", t.dataset.status === status);
  });

  if (status === "all") {
    renderTasks(allTasks);
  } else {
    renderTasks(allTasks.filter((t) => t.status === status));
  }
}

// Task Modal
function openTaskModal(taskId = null) {
  const modal = document.getElementById("task-modal");
  const titleEl = document.getElementById("task-modal-title");
  const form = document.getElementById("task-form");

  form.reset();

  if (taskId) {
    const task = allTasks.find((t) => t.id === taskId);
    if (!task) return;
    titleEl.textContent = "Edit Task";
    document.getElementById("task-id").value = task.id;
    document.getElementById("task-title").value = task.title;
    document.getElementById("task-description").value = task.description || "";
    document.getElementById("task-status").value = task.status;
    document.getElementById("task-priority").value = task.priority;
    if (task.due_date) {
      const local = new Date(task.due_date).toISOString().slice(0, 16);
      document.getElementById("task-due-date").value = local;
    }
  } else {
    titleEl.textContent = "New Task";
    document.getElementById("task-id").value = "";
  }

  modal.classList.remove("hidden");
}

function closeTaskModal(event) {
  if (event && event.target !== document.getElementById("task-modal")) return;
  document.getElementById("task-modal").classList.add("hidden");
}

async function saveTask(e) {
  e.preventDefault();
  const taskId = document.getElementById("task-id").value;
  const dueDateVal = document.getElementById("task-due-date").value;

  const payload = {
    title: document.getElementById("task-title").value.trim(),
    description: document.getElementById("task-description").value.trim(),
    status: document.getElementById("task-status").value,
    priority: document.getElementById("task-priority").value,
    due_date: dueDateVal ? new Date(dueDateVal).toISOString() : null,
  };

  const isEdit = !!taskId;
  const { ok, data } = isEdit
    ? await api(`/tasks/${taskId}`, { method: "PUT", body: JSON.stringify(payload) })
    : await api("/tasks/", { method: "POST", body: JSON.stringify(payload) });

  if (ok) {
    showToast(isEdit ? "Task updated!" : "Task created!", "success");
    document.getElementById("task-modal").classList.add("hidden");
    await loadTasks();
    if (currentPage === "dashboard") loadDashboard();
  } else {
    showToast(data.error || "Failed to save task", "error");
  }
}

// ── CONFIRM & DELETE ───────────────────────────────────────
let pendingDelete = null;

function confirmDelete(type, id) {
  pendingDelete = { type, id };
  const messages = {
    note: "Are you sure you want to delete this note? This action cannot be undone.",
    task: "Are you sure you want to delete this task? This action cannot be undone.",
  };
  document.getElementById("confirm-message").textContent = messages[type];
  document.getElementById("confirm-dialog").classList.remove("hidden");

  document.getElementById("confirm-action-btn").onclick = executeDelete;
}

function cancelConfirm(event) {
  if (event && event.target !== document.getElementById("confirm-dialog")) return;
  document.getElementById("confirm-dialog").classList.add("hidden");
  pendingDelete = null;
}

async function executeDelete() {
  if (!pendingDelete) return;
  const { type, id } = pendingDelete;

  const endpoint = type === "note" ? `/notes/${id}` : `/tasks/${id}`;
  const { ok } = await api(endpoint, { method: "DELETE" });

  document.getElementById("confirm-dialog").classList.add("hidden");
  pendingDelete = null;

  if (ok) {
    showToast(`${type === "note" ? "Note" : "Task"} deleted`, "success");
    if (type === "note") await loadNotes();
    else await loadTasks();
    if (currentPage === "dashboard") loadDashboard();
  } else {
    showToast("Failed to delete", "error");
  }
}

// ── INIT ───────────────────────────────────────────────────
function init() {
  lucide.createIcons();

  if (authToken && currentUser) {
    // Verify token is still valid
    api("/auth/profile").then(({ ok }) => {
      if (ok) {
        showApp();
      } else {
        // Token expired/invalid — clear and show auth
        logout();
      }
    });
  } else {
    showAuth();
  }
}

document.addEventListener("DOMContentLoaded", init);
