from django.contrib import admin
from .models import Point


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "owner_ru", "created_at_ru", "updated_at_ru", "location_ru")
    search_fields = ("title", "description", "owner__username")

    def title_ru(self, obj):
        return obj.title
    title_ru.short_description = "Название точки"

    def owner_ru(self, obj):
        return obj.owner.username
    owner_ru.short_description = "Владелец точки"

    def created_at_ru(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    created_at_ru.short_description = "Дата создания"

    def updated_at_ru(self, obj):
        return obj.updated_at.strftime("%d.%m.%Y %H:%M")
    updated_at_ru.short_description = "Дата обновления"

    def location_ru(self, obj):
        if obj.location:
            return f"({obj.location.y:.5f}, {obj.location.x:.5f})"
        return "-"
    location_ru.short_description = "Координаты"