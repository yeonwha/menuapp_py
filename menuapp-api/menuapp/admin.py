from django.contrib import admin

# Register your models here.

from .models import Food

class FoodAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        "price",
        "checked"
    )

admin.site.register(Food, FoodAdmin)