// Wasteland Navigator - Main JS

// Проверка авторизации
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        console.warn('Токен не найден. Используйте /api/auth/login/ для получения токена.');
    }
    return token;
}

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    
    // Добавляем эффект мерцания для заголовка
    const glitchElements = document.querySelectorAll('.glitch');
    glitchElements.forEach(el => {
        setInterval(() => {
            el.style.textShadow = Math.random() > 0.5 
                ? '0 0 10px #00ff00, 0 0 20px #00ff00' 
                : '-2px 0 10px #ff0000, 2px 0 10px #00ff00';
        }, 3000);
    });
});

// Утилита для API запросов
async function apiRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}
