"""Health check endpoint."""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache

def health_check(request):
    """Проверка здоровья приложения."""
    status = {
        "status": "healthy",
        "database": "unknown",
        "cache": "unknown",
    }
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status["database"] = "ok"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        status["status"] = "unhealthy"
    
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            status["cache"] = "ok"
        else:
            status["cache"] = "error"
            status["status"] = "unhealthy"
    except Exception as e:
        status["cache"] = f"error: {str(e)}"
        status["status"] = "unhealthy"
    
    return JsonResponse(status)
