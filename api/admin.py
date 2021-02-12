from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", )
    search_fields = ("slug",)
    list_filter = ("id",)
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", )
    search_fields = ("slug", )
    list_filter = ("id", )
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "category", "get_genres", )

    def get_genres(self, obj):
        return "\n".join([g.genre for g in obj.genre.all()])

    search_fields = ("name", )
    list_filter = ("id", )
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
