const apiUrl = "http://127.0.0.1:5000";
let token = localStorage.getItem("token");

// Elementos del DOM
const authSection = document.getElementById("auth-section");
const tasksSection = document.getElementById("tasks-section");
const authForm = document.getElementById("auth-form");
const taskForm = document.getElementById("task-form");
const taskList = document.getElementById("task-list");
const authMessage = document.getElementById("auth-message");
const loginBtn = document.getElementById("login-btn");
const registerBtn = document.getElementById("register-btn");
const logoutBtn = document.getElementById("logout-btn");

// Verificar si ya hay token al cargar la página
if (token) {
  showTasksSection();
  loadTasks();
}

// Login y Registro
authForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const url =
    loginBtn.textContent === "Iniciar Sesión"
      ? `${apiUrl}/login`
      : `${apiUrl}/register`;
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await response.json();

    if (response.ok) {
      if (url.includes("login")) {
        token = data.access_token;
        localStorage.setItem("token", token);
        showTasksSection();
        loadTasks();
      } else {
        authMessage.textContent = "Usuario registrado. Ahora inicia sesión.";
        loginBtn.textContent = "Iniciar Sesión";
        registerBtn.style.display = "block";
        authForm.reset();
      }
    } else {
      authMessage.textContent = data.message || "Error en la solicitud";
    }
  } catch (error) {
    authMessage.textContent = "Error de conexión";
  }
});

registerBtn.addEventListener("click", () => {
  loginBtn.textContent = "Registrarse";
  registerBtn.style.display = "none";
});

// Logout
logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("token");
  token = null;
  tasksSection.style.display = "none";
  authSection.style.display = "block";
  authMessage.textContent = "";
  loginBtn.textContent = "Iniciar Sesión";
  registerBtn.style.display = "block";
});

// Crear tarea
taskForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = document.getElementById("task-title").value;
  const description = document.getElementById("task-description").value;

  try {
    const response = await fetch(`${apiUrl}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title, description }),
    });
    if (response.ok) {
      taskForm.reset();
      loadTasks();
    }
  } catch (error) {
    console.error("Error al crear tarea:", error);
  }
});

// Cargar tareas
async function loadTasks() {
  try {
    const response = await fetch(`${apiUrl}/tasks`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    const tasks = await response.json();
    taskList.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.innerHTML = `${task.title} - ${task.description} <button onclick="deleteTask(${task.id})">Eliminar</button>`;
      taskList.appendChild(li);
    });
  } catch (error) {
    console.error("Error al cargar tareas:", error);
  }
}

// Eliminar tarea
async function deleteTask(taskId) {
  try {
    const response = await fetch(`${apiUrl}/tasks/${taskId}`, {
      method: "DELETE",
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.ok) {
      loadTasks();
    }
  } catch (error) {
    console.error("Error al eliminar tarea:", error);
  }
}

// Mostrar sección de tareas
function showTasksSection() {
  authSection.style.display = "none";
  tasksSection.style.display = "block";
}
