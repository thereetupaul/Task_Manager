
const API_BASE = "http://127.0.0.1:8000"


// REGISTER

async function register() {

const email = document.getElementById("email").value
const password = document.getElementById("password").value

try {
    const res = await fetch(`${API_BASE}/users/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email,
            password
        })
    });

    if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || `HTTP error! status: ${res.status}`);
    }

    const data = await res.json();
    document.getElementById("message").innerText = data.message || "Registration successful";
} catch (error) {
    console.error('Registration error:', error);
    document.getElementById("message").innerText = "Registration failed: " + error.message;
}

}



// LOGIN

async function login(){

const email = document.getElementById("email").value
const password = document.getElementById("password").value

try {
    const formData = new FormData();
    formData.append('username', email);  // OAuth2PasswordRequestForm expects 'username'
    formData.append('password', password);

    const res = await fetch(`${API_BASE}/login`,{
        method:"POST",
        body: formData  // Send as FormData, not JSON
    });

    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }

    const data = await res.json();

    if (data.access_token) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "dashboard.html";
    } else {
        document.getElementById("message").innerText = "Login failed: No token received";
    }
} catch (error) {
    console.error('Login error:', error);
    document.getElementById("message").innerText = "Login failed: " + error.message;
}

}



// GET TOKEN

function getToken(){

return localStorage.getItem("token")

}

// GET CURRENT USER

let currentUser = null;

async function getCurrentUser(){
    const token = getToken();
    if (!token) return null;

    try {
        const res = await fetch(`${API_BASE}/users/me`, {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (res.ok) {
            currentUser = await res.json();
            return currentUser;
        }
    } catch (error) {
        console.error('Error getting current user:', error);
    }
    return null;
}



// LOGOUT

function logout(){
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// DEBUG INFO

function debugInfo(){
    const token = getToken();
    alert(`Token: ${token ? token.substring(0, 20) + '...' : 'No token'}\n\nCurrent User: ${currentUser ? JSON.stringify(currentUser, null, 2) : 'Not loaded'}\n\nCheck browser console for detailed logs.`);
}



// LOAD TASKS

async function loadTasks(){

const token = getToken();
console.log('Token:', token); // Debug log

if (!token) {
    alert("Please login first");
    window.location.href = "login.html";
    return;
}

// Get current user info first
await getCurrentUser();
console.log('Current user:', currentUser); // Debug log

// Update user info display
if (currentUser) {
    document.getElementById('userEmail').textContent = currentUser.email;
    document.getElementById('userRole').textContent = currentUser.role;
    document.getElementById('userInfo').style.display = 'block';
}

try {
    console.log('Making API call to:', `${API_BASE}/tasks/`); // Debug log

    const res = await fetch(`${API_BASE}/tasks/`,{
        headers:{
            "Authorization":`Bearer ${token}`
        }
    });

    console.log('Response status:', res.status); // Debug log

    if (!res.ok) {
        const errorText = await res.text();
        console.log('Error response:', errorText); // Debug log
        throw new Error(`HTTP error! status: ${res.status} - ${errorText}`);
    }

    const tasks = await res.json();

    console.log('Loaded tasks:', tasks); // Debug log

    const list = document.getElementById("taskList");
    list.innerHTML="";

    if (tasks.length === 0) {
        list.innerHTML = "<li>No tasks found. Create your first task above!</li>";
        return;
    }

    tasks.forEach(task =>{
        const li = document.createElement("li");
        li.className = "task-item";
        li.id = `task-${task.id}`;

        // Show owner info if user is admin
        let ownerInfo = '';
        if (currentUser && currentUser.role === 'admin' && task.owner) {
            ownerInfo = `<div style="font-size: 0.8em; color: #666; margin-bottom: 5px;">Created by: ${task.owner.email}</div>`;
        }

        li.innerHTML = `
        <div>
            ${ownerInfo}
            <strong>${task.title}</strong>
            <p>${task.description || ''}</p>
            <button onclick="editTask('${task.id}')">Edit</button>
            <button onclick="deleteTask('${task.id}')">Delete</button>
        </div>
        `;

        list.appendChild(li);
    });
} catch (error) {
    console.error('Error loading tasks:', error);
    alert('Error loading tasks: ' + error.message);
}

}



// CREATE TASK

async function createTask(){

const title = document.getElementById("taskTitle").value;
const description = document.getElementById("taskDescription").value;
const status = document.getElementById("taskStatus").value;

const token = localStorage.getItem("token");

const res = await fetch("http://localhost:8000/tasks",{
method:"POST",
headers:{
"Content-Type":"application/json",
"Authorization":"Bearer " + token
},
body: JSON.stringify({
title,
description,
status
})
});

loadTasks();
}



// DELETE TASK

async function deleteTask(id){

const token = getToken();
if (!token) {
    alert("Please login first");
    window.location.href = "login.html";
    return;
}

try {
    const res = await fetch(`${API_BASE}/tasks/${id}`,{
        method:"DELETE",
        headers:{
            "Authorization":`Bearer ${token}`
        }
    });

    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }

    loadTasks();
} catch (error) {
    console.error('Error deleting task:', error);
    alert('Error deleting task: ' + error.message);
}

}


// EDIT TASK

async function editTask(id){

const taskItem = document.getElementById(`task-${id}`)
const taskDiv = taskItem.querySelector('div')

// Get current values
const currentTitle = taskDiv.querySelector('strong').textContent
const currentDescription = taskDiv.querySelector('p').textContent

taskItem.classList.add('editing')

taskDiv.innerHTML = `
<input type="text" id="edit-title-${id}" value="${currentTitle}" required>
<textarea id="edit-description-${id}" rows="3">${currentDescription}</textarea>
<button onclick="saveTask('${id}')">Save</button>
<button onclick="cancelEdit('${id}', '${currentTitle}', '${currentDescription}')">Cancel</button>
`

}

// SAVE TASK

async function saveTask(id){

const title = document.getElementById(`edit-title-${id}`).value
const description = document.getElementById(`edit-description-${id}`).value

if (!title.trim()) {
    alert("Task title is required");
    return;
}

const token = getToken();
if (!token) {
    alert("Please login first");
    window.location.href = "login.html";
    return;
}

try {
    const res = await fetch(`${API_BASE}/tasks/${id}`,{
        method:"PUT",
        headers:{
            "Content-Type":"application/json",
            "Authorization":`Bearer ${token}`
        },
        body:JSON.stringify({
            title,
            description
        })
    });

    if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
    }

    loadTasks();
} catch (error) {
    console.error('Error updating task:', error);
    alert('Error updating task: ' + error.message);
}

}

// CANCEL EDIT

function cancelEdit(id, originalTitle, originalDescription){

const taskItem = document.getElementById(`task-${id}`)
taskItem.classList.remove('editing')

const taskDiv = taskItem.querySelector('div')

taskDiv.innerHTML = `
<strong>${originalTitle}</strong>
<p>${originalDescription}</p>
<button onclick="editTask('${id}')">Edit</button>
<button onclick="deleteTask('${id}')">Delete</button>
`

}