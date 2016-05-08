from django.contrib import admin
from .models import TwotterProfile, Twoot, Favorite, ReTwoot, Notification

# Register your models here.
class TwotterProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

class TwootAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

class FavoriteAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

class ReTwootAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ('creation_date',)

admin.site.register(TwotterProfile, TwotterProfileAdmin)
admin.site.register(Twoot, TwootAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ReTwoot, ReTwootAdmin)
admin.site.register(Notification, NotificationAdmin)