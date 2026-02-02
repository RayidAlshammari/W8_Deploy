// ==================== Configuration ====================
const API_BASE_URL = '';

// ==================== State Management ====================
let users = [];
let tasks = [];

// ==================== Initialization ====================
document.addEventListener('DOMContentLoaded', () => {
    // Initialize tabs
    initializeTabs();
    
    // Load data
    loadUsers();
    loadTasks();
    
    // Priority slider handler
    const prioritySlider = document.getElementById('priority');
    if (prioritySlider) {
        prioritySlider.addEventListener('input', (e) => {
            document.getElementById('priorityValue').textContent = e.target.value;
        });
    }
});

// ==================== Tab Management ====================
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-section`).classList.add('active');
}

// ==================== Modal Management ====================
function toggleModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.toggle('active');
    
    // Reset form if closing
    if (!modal.classList.contains('active')) {
        const form = modal.querySelector('form');
        if (form) form.reset();
        if (modalId === 'taskModal') {
            document.getElementById('priorityValue').textContent = '3';
        }
    }
}

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.remove('active');
    }
});

// ==================== API: Users ====================
async function loadUsers() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/users/`);
        const data = await response.json();
        users = data.users || [];
        renderUsers(users);
    } catch (error) {
        showToast('Failed to load users', 'error');
        console.error('Error loading users:', error);
    } finally {
        showLoading(false);
    }
}

async function createUser(event) {
    event.preventDefault();
    
    const userData = {
        username: document.getElementById('username').value,
        full_name: document.getElementById('fullName').value,
        role: document.getElementById('role').value,
        profile: {
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            address: document.getElementById('address').value
        }
    };
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create user');
        }
        
        const data = await response.json();
        showToast('✅ User created successfully!', 'success');
        toggleModal('userModal');
        loadUsers(); // Reload users
    } catch (error) {
        showToast(`❌ Error: ${error.message}`, 'error');
        console.error('Error creating user:', error);
    } finally {
        showLoading(false);
    }
}

function renderUsers(usersToRender) {
    const grid = document.getElementById('usersGrid');
    
    if (usersToRender.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <h3>👥 No users found</h3>
                <p>Create your first user to get started</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = usersToRender.map(user => `
        <div class="card">
            <div class="card-header">
                <div>
                    <h3 class="card-title">👤 ${user.full_name}</h3>
                    <p style="color: var(--text-secondary); font-size: 0.9rem;">@${user.username}</p>
                </div>
                <span class="badge badge-${user.role}">${user.role.replace('_', ' ')}</span>
            </div>
            <div class="card-info">
                <p><strong>📧 Email:</strong> ${user.profile.email}</p>
                <p><strong>📱 Phone:</strong> ${user.profile.phone}</p>
                <p><strong>📍 Address:</strong> ${user.profile.address}</p>
                <p style="margin-top: 0.5rem; opacity: 0.7;"><strong>ID:</strong> ${user.id}</p>
            </div>
        </div>
    `).join('');
}

function filterUsers() {
    const roleFilter = document.getElementById('roleFilter').value;
    
    let filtered = users;
    if (roleFilter) {
        filtered = users.filter(user => user.role === roleFilter);
    }
    
    renderUsers(filtered);
}

// ==================== API: Tasks ====================
async function loadTasks() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/tasks/`);
        const data = await response.json();
        tasks = data.tasks || [];
        renderTasks(tasks);
    } catch (error) {
        showToast('Failed to load tasks', 'error');
        console.error('Error loading tasks:', error);
    } finally {
        showLoading(false);
    }
}

async function createTask(event) {
    event.preventDefault();
    
    const assignedToValue = document.getElementById('assignedTo').value;
    const taskData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        priority: parseInt(document.getElementById('priority').value),
        status: document.getElementById('status').value,
        assigned_to: assignedToValue ? parseInt(assignedToValue) : null
    };
    
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            // Extract validation error message
            let errorMsg = 'Failed to create task';
            if (errorData.detail && Array.isArray(errorData.detail)) {
                errorMsg = errorData.detail.map(err => err.msg).join(', ');
            } else if (errorData.detail) {
                errorMsg = errorData.detail;
            }
            throw new Error(errorMsg);
        }
        
        const data = await response.json();
        showToast('✅ Task created successfully!', 'success');
        toggleModal('taskModal');
        loadTasks(); // Reload tasks
    } catch (error) {
        showToast(`❌ Error: ${error.message}`, 'error');
        console.error('Error creating task:', error);
    } finally {
        showLoading(false);
    }
}

function renderTasks(tasksToRender) {
    const grid = document.getElementById('tasksGrid');
    
    if (tasksToRender.length === 0) {
        grid.innerHTML = `
            <div class="empty-state" style="grid-column: 1/-1;">
                <h3>✅ No tasks found</h3>
                <p>Create your first task to get started</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = tasksToRender.map(task => {
        const statusEmoji = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅'
        };
        
        return `
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">${task.title}</h3>
                    <span class="badge badge-${task.status}">${statusEmoji[task.status]} ${task.status.replace('_', ' ')}</span>
                </div>
                <div class="card-info">
                    <p>${task.description}</p>
                    <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center;">
                        <span class="priority-badge priority-${task.priority}">
                            ⭐ Priority ${task.priority}
                        </span>
                        ${task.assigned_to ? `<span style="opacity: 0.8;">👤 User #${task.assigned_to}</span>` : '<span style="opacity: 0.6;">Unassigned</span>'}
                    </div>
                    <p style="margin-top: 0.5rem; opacity: 0.7; font-size: 0.85rem;"><strong>Task ID:</strong> ${task.id}</p>
                </div>
            </div>
        `;
    }).join('');
}

function filterTasks() {
    const statusFilter = document.getElementById('statusFilter').value;
    const priorityFilter = document.getElementById('priorityFilter').value;
    
    let filtered = tasks;
    
    if (statusFilter) {
        filtered = filtered.filter(task => task.status === statusFilter);
    }
    
    if (priorityFilter) {
        filtered = filtered.filter(task => task.priority === parseInt(priorityFilter));
    }
    
    renderTasks(filtered);
}

// ==================== UI Utilities ====================
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.add('active');
    } else {
        loading.classList.remove('active');
    }
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}
