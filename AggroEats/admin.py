from django.contrib import admin
from .models import Score

# Register your models here.
class ScoreAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

admin.site.register(Score, ScoreAdmin)