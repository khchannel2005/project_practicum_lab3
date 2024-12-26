// Функція реєстрації
async function register() {
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    const iconUrl = document.getElementById('regIconUrl').value || 'default-icon.png';

    if (!username || !password) {
        alert('Username and password are required!');
        return;
    }

    const response = await fetch('http://localhost:5000/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, icon_url: iconUrl })
    });

    const data = await response.json();

    if (response.ok) {
        alert(data.message);
        loadUsers(); // Оновити список користувачів
    } else {
        alert(data.message);
    }
}

// Функція для завантаження користувачів
async function loadUsers() {
    const response = await fetch('http://localhost:5000/api/users');
    const users = await response.json();

    const usersList = document.getElementById('usersList');
    usersList.innerHTML = ''; // Очищення списку

    users.forEach(user => {
        const userDiv = document.createElement('div');
        userDiv.className = 'user';
        userDiv.innerHTML = `
            <img src="${user.icon_url}" alt="User Icon">
            <span>${user.username}</span>
        `;
        usersList.appendChild(userDiv);
    });
}

// Завантажити список користувачів під час завантаження сторінки
document.addEventListener('DOMContentLoaded', loadUsers);
