const taskForm = document.getElementById('task-form');
const taskList = document.getElementById('task-list');

// Fetch and display tasks
async function fetchTasks() {
    const response = await fetch('/tasks/');
    const tasks = await response.json();
    taskList.innerHTML = tasks
        .map(task => `<li>${task.title} <button onclick="deleteTask(${task.id})">Delete</button></li>`)
        .join('');
}

// Add a new task
taskForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const taskTitle = document.getElementById('task-title').value;

    const response = await fetch('/tasks/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: Date.now(), title: taskTitle }),
    });

    if (response.ok) {
        fetchTasks(); // Refresh task list
        taskForm.reset();
    }
});

// Delete a task
async function deleteTask(taskId) {
    await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
    fetchTasks(); // Refresh task list
}

// Initial fetch of tasks
fetchTasks();
