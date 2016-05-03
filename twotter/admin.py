from django.contrib import admin
from .models import TwotterProfile, Twoot

# Register your models here.
class TwotterProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

class TwootAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

admin.site.register(TwotterProfile, TwotterProfileAdmin)
admin.site.register(Twoot, TwootAdmin)