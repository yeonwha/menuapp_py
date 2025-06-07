from django.contrib import admin
from .models import Food

# Food model attributes to create by admin
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        "price",
        "checked"
    )

admin.site.register(Food, FoodAdmin)