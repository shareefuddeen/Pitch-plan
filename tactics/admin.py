
from django.contrib import admin
from .models import Formation, PlayerPosition


class PlayerPositionInline(admin.TabularInline):
    model = PlayerPosition
    extra = 1


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [PlayerPositionInline]